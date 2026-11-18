"""
AnalysisService: orchestrates the full pipeline.
  1. Validate URL (format + SSRF)
  2. Fetch and extract website content
  3. Send to LLM for analysis
  4. Build the final response
"""
import logging

from app.schemas import AnalysisResponse, BrandInfo, FullAnalysis
from app.services.website_extractor import WebsiteExtractor
from app.services.llm_service import LLMService
from app.utils.validators import is_safe_url

logger = logging.getLogger(__name__)


class AnalysisService:
    """Coordinates URL validation, extraction, and LLM analysis."""

    @staticmethod
    def analyze(url: str) -> AnalysisResponse:
        # Step 1: Validate URL (format + SSRF protection)
        safe, error = is_safe_url(url)
        if not safe:
            raise ValueError(error)

        logger.info("Fetching website content: %s", url)

        # Step 2: Fetch and extract website content
        try:
            content = WebsiteExtractor.extract(url)
        except Exception as e:
            raise ValueError(f"Could not fetch website content: {e}")

        if not content.get("main_text") or len(content["main_text"]) < 50:
            raise ValueError(
                "Website has insufficient content for analysis. "
                "The page may be JavaScript-rendered or blocked."
            )

        logger.info(
            "Extracted %d chars from %s",
            len(content["main_text"]),
            content.get("domain", ""),
        )

        # Step 3: Send to LLM
        analysis: FullAnalysis = LLMService.analyze_website(content)

        logger.info("LLM analysis complete")

        # Step 4: Build response
        return AnalysisResponse(
            success=True,
            website=url,
            brand=BrandInfo(
                name=analysis.competitor_analysis.brand_name,
                category=analysis.competitor_analysis.business_category,
                summary=analysis.competitor_analysis.business_overview,
            ),
            analysis=analysis,
        )
