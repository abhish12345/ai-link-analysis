# AI-Powered Website Link Analysis API

A **FastAPI** application that takes a website URL, extracts its content using BeautifulSoup, analyzes it with **Google Gemini**, and returns structured business, competitor, SEO, search query, and target audience insights.

---

## Live Demo

| Requirement | URL |
|---|---|
| **Live Demo** | https://ai-link-analysis-iwuq.onrender.com |
| **API Endpoint** | https://ai-link-analysis-iwuq.onrender.com/link-analysis |
| **API Documentation** | https://ai-link-analysis-iwuq.onrender.com/docs |

### Try it live

```bash
curl -X POST https://ai-link-analysis-iwuq.onrender.com/link-analysis \
  -H "Content-Type: application/json" \
  -d '{"url": "https://fastapi.tiangolo.com"}'
```

---

## Features

- **Website Content Extraction** — fetches HTML, strips noise (scripts, styles, nav), extracts titles, headings, meta, and body text
- **LLM-Powered Analysis** — Google Gemini with structured JSON output enforced via Pydantic schema
- **SSRF Protection** — blocks private/internal network addresses (localhost, 192.168.x.x, 127.0.0.1, etc.)
- **5 Analysis Sections** — competitor analysis, search queries, SEO improvements, top services, target audience
- **Error Handling** — invalid URLs, inaccessible websites, and LLM failures handled gracefully
- **Swagger Docs** — interactive API documentation at `/docs`

---

## Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Web framework + REST API |
| Uvicorn | ASGI server |
| Pydantic | Data validation + structured schema |
| httpx | HTTP client for website fetching |
| BeautifulSoup4 | HTML parsing and content extraction |
| Google Gemini (gemini-2.5-flash) | LLM for content analysis |
| google-genai SDK | Gemini API client |

---

## Project Structure

```
ai-link-analysis/
│
├── app/
│   ├── main.py                  # FastAPI app + POST /link-analysis
│   ├── config.py                # Settings from .env
│   ├── schemas.py               # Pydantic models for all 5 sections
│   ├── services/
│   │   ├── website_extractor.py # Fetch HTML + extract content with BeautifulSoup
│   │   ├── llm_service.py       # Gemini API integration
│   │   ├── analysis_service.py  # Orchestrates full pipeline
│   │   └── competitor_service.py # Competitor research helper
│   └── utils/
│       └── validators.py       # URL validation + SSRF protection
│
├── tests/
│   └── test_link_analysis.py    # Test suite (13 tests)
│
├── docs/
│   └── sample_logs.md           # Sample API responses
│
├── .env.example
├── .gitignore
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## Setup & Installation

### 1. Clone / enter the project

```bash
cd ai-link-analysis
```

### 2. Create a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure credentials

```bash
cp .env.example .env
# Edit .env and add your Gemini API key
```

Get a free Gemini API key at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### 5. Start the server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 4000 --reload
```

### 6. Open the API docs

```
http://localhost:4000/docs
```

---

## API Reference

### `POST /link-analysis`

Analyzes a website URL and returns structured business insights.

#### Request

```bash
curl -X POST http://localhost:4000/link-analysis \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

#### Response (200)

```json
{
  "success": true,
  "website": "https://fastapi.tiangolo.com",
  "brand": {
    "name": "FastAPI",
    "category": "Python Web Framework",
    "summary": "FastAPI is a modern, high-performance Python web framework for building APIs."
  },
  "analysis": {
    "competitor_analysis": {
      "brand_name": "FastAPI",
      "business_overview": "A modern, high-performance Python web framework...",
      "business_category": "Python Web Framework",
      "main_products_services": [
        "High-performance API development",
        "Automatic interactive API documentation",
        "Data validation and parsing with Pydantic",
        "Type conversion for network data",
        "Editor support with completion and type checks"
      ],
      "competitors": [
        {
          "name": "Flask",
          "main_service": "Microframework for web development",
          "strengths": ["Established ecosystem", "Large community"],
          "weaknesses": ["Lower performance", "No built-in async support"]
        },
        {
          "name": "Django",
          "main_service": "Full-stack web framework",
          "strengths": ["Batteries-included", "Built-in admin"],
          "weaknesses": ["Heavier", "Slower for API-only use cases"]
        },
        {
          "name": "Starlette",
          "main_service": "Lightweight ASGI framework",
          "strengths": ["Very fast", "Minimal"],
          "weaknesses": ["Less features", "Smaller community"]
        }
      ],
      "your_strengths": [
        "Exceptional performance, on par with NodeJS and Go",
        "200-300% faster coding speed",
        "40% fewer bugs",
        "Automatic interactive documentation",
        "Standard Python type hints"
      ],
      "competitive_advantages": [
        "Personalized service",
        "Competitive pricing"
      ],
      "opportunities": [
        "Expand content for ML deployment use cases",
        "Develop more advanced tutorials",
        "Foster community contributions"
      ]
    },
    "target_search_queries": [
      {"query": "FastAPI tutorial get started", "platforms": ["Google"], "intent": "Service Discovery", "business_relevance": "...", "target_audience": "Backend Developers"},
      {"query": "Python high performance API framework", "platforms": ["Google", "LinkedIn"], "intent": "Service Search", "business_relevance": "...", "target_audience": "Software Architects"},
      {"query": "build REST API with Python type hints", "platforms": ["Google"], "intent": "Service Search", "business_relevance": "...", "target_audience": "Python Developers"},
      {"query": "FastAPI automatic swagger docs", "platforms": ["Google"], "intent": "Business Discovery", "business_relevance": "...", "target_audience": "API Developers"},
      {"query": "FastAPI vs Flask performance", "platforms": ["Google", "X"], "intent": "Business Discovery", "business_relevance": "...", "target_audience": "Backend Engineers"}
    ],
    "seo_improvements": {
      "primary_keyword": "FastAPI Python web framework",
      "secondary_keywords": ["Python API development", "high performance API", "async Python framework", "REST API Python", "OpenAPI documentation"],
      "long_tail_keywords": ["how to build fast API with Python", "FastAPI Pydantic validation tutorial", "deploy FastAPI to production", "FastAPI microservices architecture", "automatic API docs Python framework"],
      "recommended_title": "FastAPI | High-Performance Python Web Framework for Building Robust APIs",
      "meta_description": "Build fast, robust, and production-ready APIs with FastAPI. Leverage standard Python type hints, automatic interactive documentation...",
      "supporting_content": [
        "Getting Started with FastAPI guide",
        "Building Machine Learning API with FastAPI tutorial",
        "FastAPI vs Flask vs Django comparison article",
        "Case studies from Microsoft, Uber, Netflix",
        "FAQ section on performance and async programming"
      ]
    },
    "top_services": [
      {"service_name": "High-Performance API Development", "description": "Build extremely fast APIs", "target_industry": "Technology", "target_customer": "Backend Developers", "main_benefit": "Production-ready performance"},
      {"service_name": "Automatic Interactive API Documentation", "description": "Auto-generate Swagger UI and ReDoc", "target_industry": "Technology", "target_customer": "API Developers", "main_benefit": "Zero-effort documentation"},
      {"service_name": "Robust Data Validation", "description": "Automatic validation with Pydantic", "target_industry": "Technology", "target_customer": "Backend Developers", "main_benefit": "40% fewer bugs"},
      {"service_name": "Rapid API Prototyping", "description": "200-300% faster coding speed", "target_industry": "Technology", "target_customer": "Startup Founders", "main_benefit": "Faster time to market"},
      {"service_name": "Standards-Based API Building", "description": "Compatible with OpenAPI and JSON Schema", "target_industry": "Technology", "target_customer": "Software Architects", "main_benefit": "Interoperability"}
    ],
    "target_audience": {
      "primary_audience": ["Python Developers", "Backend Engineers", "Software Architects"],
      "secondary_audience": ["Data Scientists", "DevOps Engineers", "Full-stack Developers"],
      "industries": ["Technology", "SaaS", "Data Science", "Fintech", "E-commerce", "Healthcare"],
      "business_types": ["SMBs", "Startups", "Enterprise"],
      "location_focus": "Global",
      "customer_needs": ["Building high-performance APIs", "Reducing development time", "Ensuring data validation", "Automatic documentation"],
      "customer_challenges": ["Limited IT budget", "Lack of in-house expertise"],
      "recommended_segments": [
        {"audience": "Backend Developers", "business_type": "Tech Company", "requirement": "Build fast microservices"},
        {"audience": "Data Scientists", "business_type": "AI/ML Team", "requirement": "Deploy ML models as APIs"},
        {"audience": "Software Architects", "business_type": "Enterprise IT", "requirement": "Standards-based APIs"},
        {"audience": "Startup Founders", "business_type": "Early-stage Startup", "requirement": "Rapid prototyping"},
        {"audience": "Full-stack Developers", "business_type": "Web Agency", "requirement": "Backend + frontend integration"}
      ]
    }
  }
}
```

#### Error Responses

**Invalid URL (422):**
```json
{"success": false, "error": "URL scheme must be http or https (got 'ftp')."}
```

**SSRF Blocked (422):**
```json
{"success": false, "error": "Access to 'localhost' is blocked (SSRF protection)."}
```

**Website Inaccessible (422):**
```json
{"success": false, "error": "Could not fetch website content: ..."}
```

---

## Running Tests

```bash
pytest tests/ -v
```

Expected output:

```
tests/test_link_analysis.py::test_valid_url_accepted              PASSED
tests/test_link_analysis.py::test_invalid_scheme_rejected         PASSED
tests/test_link_analysis.py::test_no_hostname_rejected            PASSED
tests/test_link_analysis.py::test_empty_url_rejected              PASSED
tests/test_link_analysis.py::test_localhost_blocked               PASSED
tests/test_link_analysis.py::test_private_ip_blocked              PASSED
tests/test_link_analysis.py::test_loopback_ip_blocked             PASSED
tests/test_link_analysis.py::test_health_check                    PASSED
tests/test_link_analysis.py::test_missing_url_field               PASSED
tests/test_link_analysis.py::test_invalid_scheme_url              PASSED
tests/test_link_analysis.py::test_localhost_blocked_by_ssrf       PASSED
tests/test_link_analysis.py::test_successful_analysis_with_mock   PASSED
tests/test_link_analysis.py::test_insufficient_content_rejected   PASSED
========================= 13 passed ==========================
```

---

## SSRF Protection

The API validates all URLs before fetching:
- **Scheme check** — only `http` and `https` allowed
- **DNS resolution** — hostname is resolved to IP
- **Private IP blocking** — blocks `127.0.0.1`, `192.168.x.x`, `10.x.x.x`, `172.16.x.x`, `169.254.x.x`, etc.
- **Internal hostname blocking** — blocks `localhost`, `0.0.0.0`, cloud metadata endpoints

---

## LLM Platform Comparison & Recommendation

### A. Platform Comparison

| Criteria | Google Gemini 2.5 Flash | OpenAI GPT-4o-mini | Anthropic Claude 3.5 Haiku |
|---|---|---|---|
| **Provider** | Google | OpenAI | Anthropic |
| **Model** | gemini-2.5-flash | gpt-4o-mini | claude-3-5-haiku |
| **Input Cost** | $0.10 / 1M tokens | $0.15 / 1M tokens | $0.10 / 1M tokens |
| **Output Cost** | $0.40 / 1M tokens | $0.60 / 1M tokens | $0.50 / 1M tokens |
| **Context Window** | 1M tokens | 128K tokens | 200K tokens |
| **JSON Support** | ✅ Native schema enforcement | ✅ JSON mode | ✅ Tool use |
| **Free Tier** | ✅ Yes (generous) | ❌ No | ❌ No |
| **Speed** | Fast (~2-5s) | Fast (~2-5s) | Fast (~2-5s) |
| **Recommendation** | ✅ **Best choice** | Good alternative | Good alternative |

### B. Best Model Selection: Google Gemini 2.5 Flash

**Selected because:**
1. **Free tier** — Google offers generous free API access, making it ideal for development and testing
2. **Lowest cost** — $0.10 input / $0.40 output per 1M tokens (cheapest among the three)
3. **Massive context window** — 1M tokens handles large website content without truncation
4. **Native JSON schema enforcement** — Gemini's `response_schema` guarantees structured output matching our Pydantic models
5. **Strong reasoning** — Gemini 2.5 Flash produces high-quality business analysis comparable to larger models

### C. Cost Optimization

| Strategy | Implementation |
|---|---|
| Content cleaning | BeautifulSoup strips scripts, styles, nav, footers before sending to LLM |
| Content truncation | Max 8,000 chars sent to LLM (configurable via `MAX_CONTENT_LENGTH`) |
| Schema enforcement | `response_schema` prevents wasted tokens on malformed output |
| Single API call | All 5 sections generated in one LLM call, not 5 separate calls |
| Model selection | Using Flash (cheapest) instead of Pro — sufficient for this analysis |
| Prompt efficiency | System prompt is concise; content is structured with headers |

### D. Final Recommendation

| Detail | Value |
|---|---|
| **Recommended Provider** | Google |
| **Recommended Model** | gemini-2.5-flash |
| **Estimated Input Tokens** | ~3,000-4,000 (website content + prompt) |
| **Estimated Output Tokens** | ~2,000-3,000 (structured JSON) |
| **Estimated Cost per Analysis** | ~$0.001-0.002 (essentially free on free tier) |
| **Expected Response Time** | 3-8 seconds |
| **Reason** | Best balance of cost, speed, accuracy, and JSON reliability |
| **Fallback Model** | OpenAI GPT-4o-mini ($0.15/$0.60 per 1M tokens) |

> **Pricing source:** Google AI pricing page (ai.google.dev/gemini-api/docs/pricing), OpenAI pricing page (platform.openai.com/pricing), Anthropic pricing page (platform.claude.com/docs/en/about-claude/pricing). Prices verified as of November 2026. Response times are estimates based on typical API behavior; actual times vary with content size and network conditions.

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GEMINI_API_KEY` | Yes | — | Google Gemini API key |
| `MAX_CONTENT_LENGTH` | No | 8000 | Max chars of website content sent to LLM |
| `REQUEST_TIMEOUT` | No | 15 | HTTP fetch timeout in seconds |

---

## Deployment

This app is deployed on **Render.com** — live at [https://ai-link-analysis-iwuq.onrender.com](https://ai-link-analysis-iwuq.onrender.com)

### Deploy your own instance

1. Set environment variable `GEMINI_API_KEY` on your hosting platform
2. Build command: `pip install -r requirements.txt`
3. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Health check: `GET /`

> Note: `$PORT` is provided automatically by Render — do not replace it with a hardcoded port number.

---

> See [`docs/sample_logs.md`](docs/sample_logs.md) for real API responses and logs.
