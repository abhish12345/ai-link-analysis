"""
Pydantic models that define:
  1. The request schema for POST /link-analysis
  2. All five analysis sections the LLM must produce
  3. The full response schema returned by the API
"""
from pydantic import BaseModel, Field
from typing import Optional


# ── Request ───────────────────────────────────────────────────────────────────

class AnalysisRequest(BaseModel):
    url: str = Field(..., description="Website URL to analyze")


# ── Section 1: Competitor Analysis ────────────────────────────────────────────

class Competitor(BaseModel):
    name: str = Field(description="Competitor brand name")
    main_service: str = Field(default="", description="Their primary service")
    strengths: list[str] = Field(default_factory=list, description="Competitor strengths")
    weaknesses: list[str] = Field(default_factory=list, description="Competitor weaknesses or gaps")


class CompetitorAnalysis(BaseModel):
    brand_name: str = Field(description="Your brand name")
    business_overview: str = Field(description="Short business overview")
    business_category: str = Field(description="Main business category")
    main_products_services: list[str] = Field(default_factory=list)
    competitors: list[Competitor] = Field(default_factory=list, description="At least 3 competitors where available")
    your_strengths: list[str] = Field(default_factory=list)
    competitive_advantages: list[str] = Field(default_factory=list)
    opportunities: list[str] = Field(default_factory=list)


# ── Section 2: Target Search Queries ──────────────────────────────────────────

class TargetSearchQuery(BaseModel):
    query: str = Field(description="Search query string")
    platforms: list[str] = Field(description="Platforms: Google, Facebook, Instagram, LinkedIn, X")
    intent: str = Field(description="Search intent: Service Search, Business Discovery, Inspiration, B2B Search, Service Discovery")
    business_relevance: str = Field(description="Why this query is relevant to the business")
    target_audience: str = Field(description="Who would use this query")


# ── Section 3: SEO Improvements ───────────────────────────────────────────────

class SEOImprovements(BaseModel):
    primary_keyword: str = Field(description="Main keyword")
    secondary_keywords: list[str] = Field(default_factory=list)
    long_tail_keywords: list[str] = Field(default_factory=list)
    relevant_business_keywords: list[str] = Field(default_factory=list)
    recommended_title: str = Field(description="SEO-optimized title")
    meta_description: str = Field(description="Recommended meta description")
    supporting_content: list[str] = Field(
        default_factory=list,
        description="Additional content suggestions: landing pages, FAQs, blog topics, etc."
    )


# ── Section 4: Top 5 Services ────────────────────────────────────────────────

class TopService(BaseModel):
    service_name: str = Field(description="Name of the service")
    description: str = Field(description="Short service explanation")
    target_industry: str = Field(description="Relevant business industry")
    target_customer: str = Field(description="Potential customer type")
    main_benefit: str = Field(description="Why customers need this service")


# ── Section 5: Target Audience ────────────────────────────────────────────────

class AudienceSegment(BaseModel):
    audience: str = Field(description="Audience label")
    business_type: str = Field(description="Type of business")
    requirement: str = Field(description="Their need or requirement")


class TargetAudience(BaseModel):
    primary_audience: list[str] = Field(default_factory=list)
    secondary_audience: list[str] = Field(default_factory=list)
    industries: list[str] = Field(default_factory=list)
    business_types: list[str] = Field(default_factory=list)
    location_focus: str = Field(default="", description="Geographical focus if available")
    customer_needs: list[str] = Field(default_factory=list)
    customer_challenges: list[str] = Field(default_factory=list)
    customer_interests: list[str] = Field(default_factory=list, description="Potential customer interests")
    recommended_segments: list[AudienceSegment] = Field(default_factory=list)


# ── Full Analysis (all 5 sections) ───────────────────────────────────────────

class FullAnalysis(BaseModel):
    competitor_analysis: CompetitorAnalysis
    target_search_queries: list[TargetSearchQuery] = Field(
        description="Exactly 5 search queries"
    )
    seo_improvements: SEOImprovements
    top_services: list[TopService] = Field(description="Exactly 5 services")
    target_audience: TargetAudience


# ── API Response ─────────────────────────────────────────────────────────────

class BrandInfo(BaseModel):
    name: str
    category: str
    summary: str


class AnalysisResponse(BaseModel):
    success: bool
    website: str
    brand: BrandInfo
    analysis: FullAnalysis
