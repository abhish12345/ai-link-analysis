"""
Tests for the /link-analysis endpoint and utility functions.
Run with:
    pytest tests/ -v
"""
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, MagicMock

from app.main import app
from app.utils.validators import is_valid_url, is_safe_url


# ── URL Validation Tests ──────────────────────────────────────────────────────

def test_valid_url_accepted():
    valid, msg = is_valid_url("https://example.com")
    assert valid is True
    assert msg == ""


def test_invalid_scheme_rejected():
    valid, msg = is_valid_url("ftp://example.com")
    assert valid is False
    assert "http or https" in msg


def test_no_hostname_rejected():
    valid, msg = is_valid_url("https://")
    assert valid is False
    assert "hostname" in msg.lower()


def test_empty_url_rejected():
    valid, msg = is_valid_url("")
    assert valid is False


# ── SSRF Protection Tests ─────────────────────────────────────────────────────

def test_localhost_blocked():
    safe, msg = is_safe_url("http://localhost:4000")
    assert safe is False
    assert "SSRF" in msg or "blocked" in msg


def test_private_ip_blocked():
    safe, msg = is_safe_url("http://192.168.1.1")
    assert safe is False
    assert "SSRF" in msg or "private" in msg.lower()


def test_loopback_ip_blocked():
    safe, msg = is_safe_url("http://127.0.0.1")
    assert safe is False
    assert "SSRF" in msg or "private" in msg.lower()


# ── API Endpoint Tests ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_missing_url_field():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/link-analysis", json={})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_invalid_scheme_url():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/link-analysis", json={"url": "ftp://bad-scheme.com"})
    assert resp.status_code == 422
    assert resp.json()["success"] is False


@pytest.mark.asyncio
async def test_localhost_blocked_by_ssrf():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/link-analysis", json={"url": "http://localhost:8080"})
    assert resp.status_code == 422
    assert resp.json()["success"] is False
    assert "SSRF" in resp.json()["error"]


@pytest.mark.asyncio
async def test_successful_analysis_with_mock():
    """Test the full endpoint with mocked LLM and extractor."""
    from app.schemas import (
        AnalysisResponse, BrandInfo, FullAnalysis,
        CompetitorAnalysis, Competitor, SEOImprovements,
        TargetSearchQuery, TopService, TargetAudience, AudienceSegment
    )

    mock_content = {"title": "Test", "meta_description": "Test", "headings": ["Test"], "main_text": "x"*100, "domain": "example.com", "url": "https://example.com"}

    mock_analysis = FullAnalysis(
        competitor_analysis=CompetitorAnalysis(
            brand_name="Test Brand",
            business_overview="A test company",
            business_category="Technology",
            main_products_services=["Service A"],
            competitors=[
                Competitor(name="Comp 1", main_service="Dev", strengths=[], weaknesses=[]),
                Competitor(name="Comp 2", main_service="Dev", strengths=[], weaknesses=[]),
                Competitor(name="Comp 3", main_service="Dev", strengths=[], weaknesses=[]),
            ],
            your_strengths=["Strength"],
            competitive_advantages=["Advantage"],
            opportunities=["Opportunity"],
        ),
        target_search_queries=[
            TargetSearchQuery(query=f"Query {i}", platforms=["Google"], intent="Search", business_relevance="Relevant", target_audience="Audience")
            for i in range(5)
        ],
        seo_improvements=SEOImprovements(
            primary_keyword="test",
            secondary_keywords=["test2"],
            recommended_title="Test Title",
            meta_description="Test meta",
            supporting_content=["Blog"],
        ),
        top_services=[
            TopService(service_name=f"Service {i}", description="Desc", target_industry="Tech", target_customer="SMB", main_benefit="Benefit")
            for i in range(5)
        ],
        target_audience=TargetAudience(
            primary_audience=["SMBs"],
            secondary_audience=["Startups"],
            industries=["Tech"],
            customer_needs=["Websites"],
            customer_interests=["Web design"],
            recommended_segments=[
                AudienceSegment(audience="SMBs", business_type="Small Business", requirement="Web")
            ],
        ),
    )

    with patch("app.services.analysis_service.WebsiteExtractor.extract", return_value=mock_content), \
         patch("app.services.analysis_service.LLMService.analyze_website", return_value=mock_analysis):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post("/link-analysis", json={"url": "https://example.com"})

    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["website"] == "https://example.com"
    assert data["brand"]["name"] == "Test Brand"
    assert len(data["analysis"]["target_search_queries"]) == 5
    assert len(data["analysis"]["top_services"]) == 5
    assert len(data["analysis"]["competitor_analysis"]["competitors"]) >= 3


@pytest.mark.asyncio
async def test_insufficient_content_rejected():
    """Website with too little content should return 422."""
    mock_content = {"title": "", "meta_description": "", "headings": [], "main_text": "tiny", "domain": "example.com", "url": "https://example.com"}

    with patch("app.services.analysis_service.WebsiteExtractor.extract", return_value=mock_content):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post("/link-analysis", json={"url": "https://example.com"})

    assert resp.status_code == 422
    assert "insufficient" in resp.json()["error"].lower()
