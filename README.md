# AI-Powered Website Link Analysis API

A **FastAPI** application that takes a website URL, extracts its content using BeautifulSoup, analyzes it with **Google Gemini**, and returns structured business, competitor, SEO, search query, and target audience insights.

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
│   └── test_link_analysis.py    # Test suite (9 tests)
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
  "website": "https://example.com",
  "brand": {
    "name": "Example Corp",
    "category": "Technology Services",
    "summary": "A technology company providing digital solutions."
  },
  "analysis": {
    "competitor_analysis": {
      "brand_name": "Example Corp",
      "business_overview": "...",
      "business_category": "Technology Services",
      "main_products_services": ["..."],
      "competitors": [
        {"name": "Competitor A", "main_service": "...", "strengths": [], "weaknesses": []}
      ],
      "your_strengths": [],
      "competitive_advantages": [],
      "opportunities": []
    },
    "target_search_queries": [
      {"query": "...", "platforms": ["Google"], "intent": "Service Search", "business_relevance": "...", "target_audience": "..."}
    ],
    "seo_improvements": {
      "primary_keyword": "...",
      "secondary_keywords": [],
      "long_tail_keywords": [],
      "recommended_title": "...",
      "meta_description": "...",
      "supporting_content": []
    },
    "top_services": [
      {"service_name": "...", "description": "...", "target_industry": "...", "target_customer": "...", "main_benefit": "..."}
    ],
    "target_audience": {
      "primary_audience": [],
      "secondary_audience": [],
      "industries": [],
      "customer_needs": [],
      "recommended_segments": []
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

This app is ready for deployment on Render, Railway, or any platform that supports Python:

1. Set environment variable `GEMINI_API_KEY` on your hosting platform
2. Build command: `pip install -r requirements.txt`
3. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Health check: `GET /`

---

> See [`docs/sample_logs.md`](docs/sample_logs.md) for real API responses and logs.
