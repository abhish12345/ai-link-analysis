# Sample API Logs & Responses

## Server Startup

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:4000 (Press CTRL+C to quit)
```

---

## Sample Request

```bash
curl -X POST http://localhost:4000/link-analysis \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

---

## Sample Response (200)

```json
{
  "success": true,
  "website": "https://example.com",
  "brand": {
    "name": "Example Corp",
    "category": "Technology Services",
    "summary": "A technology company providing digital solutions and web services."
  },
  "analysis": {
    "competitor_analysis": {
      "brand_name": "Example Corp",
      "business_overview": "Example Corp provides technology services...",
      "business_category": "Technology Services",
      "main_products_services": ["Web Development", "Cloud Solutions", "Consulting"],
      "competitors": [
        {
          "name": "Competitor A",
          "main_service": "Web Development",
          "strengths": ["Established brand", "Large team"],
          "weaknesses": ["High pricing", "Slow response"]
        },
        {
          "name": "Competitor B",
          "main_service": "Cloud Solutions",
          "strengths": ["Wide product range"],
          "weaknesses": ["Limited support"]
        },
        {
          "name": "Competitor C",
          "main_service": "Consulting",
          "strengths": ["Strong reputation"],
          "weaknesses": ["Niche focus only"]
        }
      ],
      "your_strengths": ["Affordable solutions", "Fast delivery"],
      "competitive_advantages": ["Personalized service", "Competitive pricing"],
      "opportunities": ["Expand online visibility", "Enter new markets"]
    },
    "target_search_queries": [
      {
        "query": "Best technology services company",
        "platforms": ["Google", "LinkedIn"],
        "intent": "Service Search",
        "business_relevance": "Directly matches core service",
        "target_audience": "Business owners seeking tech solutions"
      },
      {
        "query": "Affordable web development services",
        "platforms": ["Google", "Facebook"],
        "intent": "Service Discovery",
        "business_relevance": "Highlights pricing advantage",
        "target_audience": "Small businesses"
      },
      {
        "query": "Technology consulting for startups",
        "platforms": ["LinkedIn"],
        "intent": "B2B Search",
        "business_relevance": "Targets startup segment",
        "target_audience": "Startup founders"
      },
      {
        "query": "Cloud solutions provider",
        "platforms": ["Google", "X"],
        "intent": "Service Search",
        "business_relevance": "Core service offering",
        "target_audience": "IT decision makers"
      },
      {
        "query": "Digital transformation services",
        "platforms": ["Instagram", "LinkedIn"],
        "intent": "Business Discovery",
        "business_relevance": "Broad service category",
        "target_audience": "Enterprise companies"
      }
    ],
    "seo_improvements": {
      "primary_keyword": "technology services",
      "secondary_keywords": ["web development", "cloud solutions", "tech consulting"],
      "long_tail_keywords": ["affordable web development for small businesses", "cloud migration services for startups"],
      "recommended_title": "Example Corp | Technology Services, Web Development & Cloud Solutions",
      "meta_description": "Example Corp provides affordable technology services including web development, cloud solutions, and consulting for businesses of all sizes.",
      "supporting_content": [
        "Service landing pages for each core service",
        "Case studies showcasing client success",
        "FAQ page addressing common client questions",
        "Blog posts on technology trends",
        "Location-based landing pages for key markets"
      ]
    },
    "top_services": [
      {
        "service_name": "Web Development",
        "description": "Custom website and web application development",
        "target_industry": "All industries",
        "target_customer": "Small to medium businesses",
        "main_benefit": "Professional online presence that drives leads"
      },
      {
        "service_name": "Cloud Solutions",
        "description": "Cloud migration, hosting, and infrastructure management",
        "target_industry": "Technology, Finance",
        "target_customer": "IT departments, CTOs",
        "main_benefit": "Scalable infrastructure with reduced costs"
      },
      {
        "service_name": "Technology Consulting",
        "description": "Strategic technology planning and advisory",
        "target_industry": "All industries",
        "target_customer": "Business owners, executives",
        "main_benefit": "Expert guidance on technology investments"
      },
      {
        "service_name": "Digital Transformation",
        "description": "End-to-end digital modernization of business processes",
        "target_industry": "Enterprise, Retail",
        "target_customer": "Enterprise companies",
        "main_benefit": "Improved efficiency and competitive advantage"
      },
      {
        "service_name": "IT Support",
        "description": "Ongoing technical support and maintenance",
        "target_industry": "All industries",
        "target_customer": "SMBs without in-house IT",
        "main_benefit": "Reliable tech support without staffing costs"
      }
    ],
    "target_audience": {
      "primary_audience": ["Small and medium businesses", "Startups"],
      "secondary_audience": ["Enterprise companies", "Retail businesses"],
      "industries": ["Technology", "Retail", "Finance", "Healthcare"],
      "business_types": ["SMBs", "Startups", "Enterprise", "Professional Services"],
      "location_focus": "Global",
      "customer_needs": ["Affordable web development", "Cloud migration", "Digital transformation"],
      "customer_challenges": ["Limited IT budget", "Lack of in-house expertise", "Need for fast delivery"],
      "recommended_segments": [
        {"audience": "Small Businesses", "business_type": "SMB", "requirement": "Website Development"},
        {"audience": "Startups", "business_type": "Startup", "requirement": "Digital Solutions"},
        {"audience": "Enterprise Companies", "business_type": "Enterprise", "requirement": "Custom Software"},
        {"audience": "Retail Businesses", "business_type": "Retail", "requirement": "E-commerce Solutions"},
        {"audience": "Professional Services", "business_type": "Services", "requirement": "Online Presence"}
      ]
    }
  }
}
```

---

## Error Responses

### Invalid URL (422)
```json
{"success": false, "error": "URL scheme must be http or https (got 'ftp')."}
```

### SSRF Blocked (422)
```json
{"success": false, "error": "Access to 'localhost' is blocked (SSRF protection)."}
```

### Private IP Blocked (422)
```json
{"success": false, "error": "URL resolves to a private/internal IP address (SSRF protection)."}
```

### Website Inaccessible (422)
```json
{"success": false, "error": "Could not fetch website content: [HTTP 403 Forbidden]"}
```

### Insufficient Content (422)
```json
{"success": false, "error": "Website has insufficient content for analysis. The page may be JavaScript-rendered or blocked."}
```

---

## Server Logs

```
2026-11-18 12:35:00  INFO     app.main — Link analysis request: https://example.com
2026-11-18 12:35:00  INFO     app.services.analysis_service — Fetching website content: https://example.com
2026-11-18 12:35:01  INFO     app.services.analysis_service — Extracted 5234 chars from example.com
2026-11-18 12:35:01  INFO     app.services.llm_service — Sending content to Gemini for analysis
2026-11-18 12:35:06  INFO     app.services.llm_service — LLM response received, length: 4521 chars
2026-11-18 12:35:06  INFO     app.services.analysis_service — LLM analysis complete
INFO:     127.0.0.1:52341 - "POST /link-analysis HTTP/1.1" 200 OK
```
