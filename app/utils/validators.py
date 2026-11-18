"""
URL validation with SSRF protection.
Blocks private/internal network addresses before any HTTP request is made.
"""
import ipaddress
import socket
from urllib.parse import urlparse

# Schemes that are safe to fetch
ALLOWED_SCHEMES = {"http", "https"}


def is_valid_url(url: str) -> tuple[bool, str]:
    """
    Validate the URL format and scheme.
    Returns (is_valid, error_message).
    """
    if not url or not isinstance(url, str):
        return False, "URL is required."

    parsed = urlparse(url)

    if parsed.scheme not in ALLOWED_SCHEMES:
        return False, f"URL scheme must be http or https (got '{parsed.scheme}')."

    if not parsed.hostname:
        return False, "URL must contain a hostname."

    return True, ""


def is_safe_url(url: str) -> tuple[bool, str]:
    """
    SSRF protection — resolve the hostname and block private/internal IPs.
    Returns (is_safe, error_message).
    """
    valid, msg = is_valid_url(url)
    if not valid:
        return False, msg

    parsed = urlparse(url)
    hostname = parsed.hostname

    # Block obvious internal patterns
    internal_hostnames = {"localhost", "0.0.0.0", "metadata.google.internal"}
    if hostname.lower() in internal_hostnames:
        return False, f"Access to '{hostname}' is blocked (SSRF protection)."

    # Resolve DNS and check the IP
    try:
        infos = socket.getaddrinfo(hostname, None)
        for info in infos:
            ip_str = info[4][0]
            ip = ipaddress.ip_address(ip_str)

            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
                return False, f"URL resolves to a private/internal IP address (SSRF protection)."

    except socket.gaierror:
        return False, f"Could not resolve hostname '{hostname}'."
    except Exception:
        return False, f"URL validation failed for '{hostname}'."

    return True, ""
