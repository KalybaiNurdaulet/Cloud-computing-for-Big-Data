"""
processor.py — B2B AI Lead Intelligence Engine
Business/AI layer. No Streamlit imports. Pure Python.

Mandatory Pivot modifications:
 - Strict security: No hard-coded API key.
 - Simple init logic.
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime, timezone

from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, ValidationError

load_dotenv()

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

LOG_FILE = os.path.join(os.path.dirname(__file__), "activity.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8")],
)
logger = logging.getLogger("lead_intelligence")

# ---------------------------------------------------------------------------
# FinOps Pricing
# ---------------------------------------------------------------------------
INPUT_COST_PER_TOKEN = 0.59 / 1_000_000
OUTPUT_COST_PER_TOKEN = 0.79 / 1_000_000


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

class LeadAnalysis(BaseModel):
    client_name: str
    project_summary: str
    estimated_budget: str
    priority_score: int
    red_flags: list[str]


@dataclass
class UsageStats:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost_usd: float

    @property
    def cost_display(self) -> str:
        return f"${self.estimated_cost_usd:.6f}"


SYSTEM_PROMPT = """
You are a B2B Lead Intelligence Engine for an SME sales team.
Your sole task is to analyze a raw business inquiry and return a SINGLE valid JSON object.
Do NOT include any text, explanation, or markdown — only the raw JSON.

The JSON must strictly follow this schema:
{
  "client_name":       "<string — company or person name, or 'Unknown' if not found>",
  "project_summary":   "<string — one sentence describing what the client wants>",
  "estimated_budget":  "<string — numeric value with currency, or 'Not specified'>",
  "priority_score":    <integer 1–10, where 10 = highest urgency + feasibility>,
  "red_flags":         ["<string>", ...]
}

Priority scoring rubric:
  - Budget mentioned and realistic → +3
  - Clear timeline/deadline → +2
  - Decision-maker identified → +2
  - Vague requirements → -2
  - Unrealistic deadline (e.g. 'by tomorrow') → -1 and add to red_flags
  - No budget, no timeline → score ≤ 4

If the input is nonsensical, irrelevant, or contains no business context, return:
{
  "client_name": "Unknown",
  "project_summary": "Input does not contain a valid business inquiry.",
  "estimated_budget": "Not specified",
  "priority_score": 1,
  "red_flags": ["Input is not a valid business inquiry."]
}
""".strip()


def analyze_lead(
    inquiry_text: str,
    api_key: str | None = None,
) -> tuple[LeadAnalysis | None, str | None, UsageStats | None]:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Use explicitly passed key from UI; fallback to .env variable
    user_provided_key = api_key or os.getenv("GROQ_API_KEY")

    if not user_provided_key:
        msg = "No API key provided. Please enter your API key in the sidebar."
        logger.error("Session [%s] | Status: ERROR | Reason: %s", timestamp, msg)
        return None, msg, None

    try:
        client = Groq(api_key=user_provided_key)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Inquiry:\n{inquiry_text}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
        )
    except Exception as exc:
        msg = f"Groq API error: {exc}"
        logger.error("Session [%s] | Status: ERROR | Reason: %s", timestamp, msg)
        return None, msg, None
        
    if not response.choices:
        msg = "The model returned an empty response."
        logger.error("Session [%s] | Status: ERROR | Reason: %s", timestamp, msg)
        return None, msg, None

    raw = response.choices[0].message.content

    # FinOps metrics
    usage = response.usage
    prompt_tokens = usage.prompt_tokens if usage else 0
    completion_tokens = usage.completion_tokens if usage else 0
    total_tokens = usage.total_tokens if usage else 0
    
    cost = (prompt_tokens * INPUT_COST_PER_TOKEN) + (completion_tokens * OUTPUT_COST_PER_TOKEN)
    stats = UsageStats(prompt_tokens, completion_tokens, total_tokens, cost)

    # Decode JSON
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        msg = f"The model returned non-JSON output:\n\n{raw}"
        logger.error("Session [%s] | Status: ERROR | Reason: JSON parse failed", timestamp)
        return None, msg, stats

    # Guard bounds check
    raw_score = data.get("priority_score")
    if not isinstance(raw_score, int) or not (1 <= raw_score <= 10):
        msg = f"Validation Error: 'priority_score' must be 1-10. Got: {raw_score}"
        logger.error("Session [%s] | Status: VALIDATION ERROR | Reason: %s", timestamp, msg)
        return None, msg, stats

    # Pydantic compile
    try:
        lead = LeadAnalysis(**data)
    except ValidationError as exc:
        msg = f"Validation Error: Schema mismatch — {exc}"
        logger.error("Session [%s] | Status: VALIDATION ERROR | Reason: %s", timestamp, msg)
        return None, msg, stats

    logger.info("Session [%s] | Status: SUCCESS | Score: %d", timestamp, lead.priority_score)
    return lead, None, stats
