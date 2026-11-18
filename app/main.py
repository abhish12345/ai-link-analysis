import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.schemas import AnalysisRequest, AnalysisResponse
from app.services.analysis_service import AnalysisService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI-Powered Website Link Analysis API",
    description=(
        "Analyzes a given website URL, understands its content using an LLM "
        "(Google Gemini), and generates business, competitor, SEO, search query, "
        "and target audience insights."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle validation/SSRF/fetch errors with clean JSON."""
    return JSONResponse(
        status_code=422,
        content={"success": False, "error": str(exc)},
    )


@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception):
    """Catch-all for unexpected errors."""
    logger.error("Unhandled error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": f"Internal server error: {exc}"},
    )


@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "ok",
        "message": "AI-Powered Website Link Analysis API is running.",
        "docs": "/docs",
    }


@app.post(
    "/link-analysis",
    response_model=AnalysisResponse,
    summary="Analyze a website URL and generate business insights",
    tags=["Analysis"],
    responses={
        200: {"description": "Analysis successful — returns all 5 sections."},
        422: {"description": "Invalid URL, SSRF blocked, or website inaccessible."},
        500: {"description": "Internal server error."},
    },
)
async def link_analysis(request: AnalysisRequest) -> AnalysisResponse:
    """
    Accepts a **website URL**, extracts its content, sends it to Google Gemini
    for analysis, and returns structured JSON with:

    1. **Competitor vs Your Brand** — brand overview, competitors, strengths, opportunities
    2. **Top 5 Target Search Queries** — for Google, Facebook, Instagram, LinkedIn, X
    3. **SEO Improvements** — keywords, title, meta description, supporting content
    4. **Top 5 Services** — identified from actual website content
    5. **Target Audience** — primary/secondary audience, industries, needs, segments

    **SSRF Protection:** Private and internal network URLs are blocked.
    """
    logger.info("Link analysis request: %s", request.url)
    return AnalysisService.analyze(request.url)
