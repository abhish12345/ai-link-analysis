"""
LLMService: sends cleaned website content to Google Gemini and receives
structured JSON analysis using Pydantic schema enforcement.

Uses the google-genai SDK with response_schema for guaranteed JSON output.
"""
import json
import logging
from google import genai
from google.genai import types
from pydantic import ValidationError

from app.config import settings
from app.schemas import FullAnalysis

logger = logging.getLogger(__name__)


# The system prompt instructs Gemini on what to produce
SYSTEM_PROMPT = """You are a business intelligence analyst. You analyze website content and produce
structured business, competitor, SEO, search query, and target audience insights.

Rules:
1. Base ALL analysis on the provided website content. Do NOT generate generic results.
2. Identify at least 3 competitors where reliable information is available. If fewer are known,
   clearly label them as AI-suggested.
3. Do NOT invent Google or social media search volumes.
4. Generate exactly 5 target search queries and 5 top services.
5. All competitor information should be clearly marked as AI-generated suggestions unless verified.
6. SEO recommendations must be practical and specific to the website's industry.
7. Return valid JSON matching the provided schema exactly."""


class LLMService:
    """Wraps the Gemini API call with structured output enforcement."""

    @staticmethod
    def analyze_website(website_content: dict) -> FullAnalysis:
        """
        Send website content to Gemini and return validated FullAnalysis.

        Raises:
            ValueError: if Gemini API key is missing or response is invalid.
            Exception: on API errors.
        """
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured.")

        client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
            http_options=types.HttpOptions(api_version="v1beta"),
        )

        # Build the user prompt with extracted content
        content_text = f"""
Website URL: {website_content.get("url", "")}
Domain: {website_content.get("domain", "")}
Page Title: {website_content.get("title", "")}
Meta Description: {website_content.get("meta_description", "")}

Headings:
{chr(10).join(f"- {h}" for h in website_content.get("headings", []))}

Page Content:
{website_content.get("main_text", "")}

Analyze this website and produce a complete business analysis with:
1. Competitor analysis (brand name, overview, category, competitors with strengths/weaknesses, your advantages, opportunities)
2. Exactly 5 target search queries with platforms, intent, relevance, and audience
3. SEO improvements (primary/secondary/long-tail keywords, SEO title, meta description, supporting content)
4. Exactly 5 top services with name, description, target industry, target customer, main benefit
5. Target audience identification (primary/secondary audience, industries, business types, location, needs, challenges, recommended segments)
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=content_text,
                config={
                    "system_instruction": SYSTEM_PROMPT,
                    "response_mime_type": "application/json",
                    "response_schema": FullAnalysis,
                },
            )

            # The response text is guaranteed JSON because of response_schema
            raw_json = response.text
            logger.info("LLM response received, length: %d chars", len(raw_json))

            # Validate with Pydantic
            analysis = FullAnalysis.model_validate_json(raw_json)
            return analysis

        except ValidationError as e:
            logger.error("LLM response did not match schema: %s", e)
            raise ValueError(f"LLM returned invalid structured data: {e}")
        except Exception as e:
            logger.error("Gemini API error: %s", e)
            raise
