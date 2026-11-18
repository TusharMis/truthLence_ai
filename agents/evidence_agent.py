"""
TruthLens AI - Evidence Agent
=============================
Agent 02 in the Multi-Agent Pipeline.
Responsibilities:
- Analyzes live search citations against the claim propositions using Google Gemini.
- Classifies evidence into SUPPORTING, OPPOSING, or CONTEXT.
- Validates domain credibility and extracts relevant factual excerpts.
"""

import logging
from typing import List, Dict, Any
from core.models import SubClaim, EvidenceItem, FactCheckState
from core.llm import GeminiClient
from tools.search_tools import is_trusted_domain, extract_domain

logger = logging.getLogger(__name__)


class EvidenceAgent:
    """
    Evidence Agent:
    Uses Gemini to categorize gathered web intelligence into Supporting and Opposing evidence.
    """

    def __init__(self, llm_client: GeminiClient):
        self.llm = llm_client
        self.name = "Evidence Agent"

    def evaluate_evidence(
        self,
        claim: str,
        subclaims: List[SubClaim],
        raw_results: List[Dict[str, Any]],
        state: FactCheckState
    ) -> List[EvidenceItem]:
        """
        Evaluates and classifies raw search hits into structured Supporting/Opposing EvidenceItems.
        """
        state.agent_logs.append(f"[{self.name}] Analyzing {len(raw_results)} web citations with Gemini for supporting vs opposing stance...")

        if not raw_results:
            state.agent_logs.append(f"[{self.name}] No live search results found to analyze.")
            return []

        # Prepare source batch for Gemini analysis (up to 10 authentic citations)
        sources_summary = []
        for idx, r in enumerate(raw_results[:10]):
            sources_summary.append({
                "source_index": idx,
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "domain": r.get("domain", extract_domain(r.get("url", ""))),
                "snippet": r.get("snippet", "")[:400]
            })

        evidence_prompt = f"""
You are a senior evidence verification analyst.
Analyze these authentic live web search results in relation to the main claim:
Main Claim: "{claim}"

Web Sources:
{sources_summary}

For each source, determine:
1. 'stance_tag':
   - 'SUPPORTING': Source affirms, corroborates, or provides scientific evidence for the claim.
   - 'OPPOSING': Source refutes, debunks, contradicts, or limits the claim (e.g., explains it does NOT give superior night vision, or that it is a myth/exaggeration).
   - 'CONTEXT': Source provides historical background (e.g. WWII British RAF radar propaganda origin), biological mechanism (vitamin A/rhodopsin), or neutral context.
2. 'key_excerpt': A concise 1-2 sentence factual excerpt explaining what this specific source states, clearly distinguishing established facts from interpretations or folklore.

Respond with ONLY a JSON array formatted like:
[
  {{
    "source_index": 0,
    "stance_tag": "SUPPORTING" | "OPPOSING" | "CONTEXT",
    "key_excerpt": "Precise factual finding from the source"
  }}
]
"""
        classified_map = {}
        try:
            analysis = self.llm.generate_json(evidence_prompt)
            if isinstance(analysis, dict) and "results" in analysis:
                analysis = analysis["results"]
            if isinstance(analysis, list):
                for item in analysis:
                    s_idx = item.get("source_index")
                    if s_idx is not None and isinstance(s_idx, int):
                        classified_map[s_idx] = {
                            "stance_tag": item.get("stance_tag", "SUPPORTING").upper(),
                            "key_excerpt": item.get("key_excerpt", "")
                        }
        except Exception as e:
            logger.warning(f"Evidence classification fallback: {e}")

        # Assemble typed EvidenceItem objects preserving 100% source traceability
        structured_evidence: List[EvidenceItem] = []
        for idx, r in enumerate(raw_results[:10]):
            url = r.get("url", "")
            domain = r.get("domain") or extract_domain(url)
            trusted = r.get("is_trusted", is_trusted_domain(url))
            
            c_info = classified_map.get(idx, {})
            stance = c_info.get("stance_tag", "SUPPORTING")
            if stance not in ("SUPPORTING", "OPPOSING", "CONTEXT"):
                stance = "SUPPORTING"
            
            excerpt = c_info.get("key_excerpt") or r.get("snippet", "")
            
            structured_evidence.append(EvidenceItem(
                title=r.get("title", "Web Source"),
                url=url,
                snippet=excerpt,
                domain=domain,
                is_trusted_domain=trusted,
                stance_tag=stance
            ))

        state.evidence = structured_evidence
        supporting_count = sum(1 for e in structured_evidence if e.stance_tag == "SUPPORTING")
        opposing_count = sum(1 for e in structured_evidence if e.stance_tag == "OPPOSING")
        state.agent_logs.append(
            f"[{self.name}] Categorized evidence: {supporting_count} Supporting, "
            f"{opposing_count} Opposing, {len(structured_evidence) - supporting_count - opposing_count} Context."
        )
        return structured_evidence
