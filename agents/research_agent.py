"""
TruthLens AI - Research Agent
=============================
Agent 01 in the Multi-Agent Pipeline.
Responsibilities:
- Analyzes and deconstructs the user's input claim into verifiable atomic sub-claims.
- Formulates balanced, neutral search queries.
- Dispatches queries to Tavily Search API to gather authentic live web citations.
"""

import logging
from typing import List, Dict, Any
from core.models import SubClaim, FactCheckState
from core.llm import GeminiClient
from tools.search_tools import SearchEngine

logger = logging.getLogger(__name__)


class ResearchAgent:
    """
    Research Agent:
    Deconstructs complex assertions and performs live web intelligence gathering via Tavily.
    """

    def __init__(self, llm_client: GeminiClient, search_engine: SearchEngine):
        self.llm = llm_client
        self.search = search_engine
        self.name = "Research Agent"

    def analyze_and_search(self, claim: str, state: FactCheckState) -> List[SubClaim]:
        """
        Decomposes the raw claim using Gemini and executes live searches with Tavily.
        Populates state.subclaims and state.raw_search_results.
        """
        state.agent_logs.append(f"[{self.name}] Analyzing claim structure and extracting atomic propositions...")

        # 1. Prompt Gemini to extract atomic sub-claims, historical nuances, and targeted search queries
        decomp_prompt = f"""
You are a senior forensic research investigator.
Deconstruct this user claim or research question into 1 to 3 atomic, testable factual propositions.
Ensure you distinguish established scientific/historical facts from popular interpretations, folklore, or propaganda:
- Proposition 1: The core direct factual or scientific claim (e.g. biological mechanism, physical effect).
- Proposition 2: The historical origin, context, or common misconception/myth dimension if applicable.

For each proposition, formulate 2 distinct, highly targeted search queries:
- Query A: Objective factual / scientific verification query
- Query B: Critical fact-checking / myth-investigation / historical origin query

Claim: "{claim}"

Respond with ONLY a JSON array of objects with this schema:
[
  {{
    "id": "C1",
    "statement": "The atomic factual assertion to test",
    "entities": ["entity1", "entity2"],
    "search_queries": ["objective factual query", "critical fact check or historical origin query"]
  }}
]
"""
        subclaims: List[SubClaim] = []
        try:
            raw_subclaims = self.llm.generate_json(decomp_prompt)
            if isinstance(raw_subclaims, dict) and "subclaims" in raw_subclaims:
                raw_subclaims = raw_subclaims["subclaims"]

            if isinstance(raw_subclaims, list):
                for idx, sc in enumerate(raw_subclaims):
                    cid = sc.get("id") or f"C{idx + 1}"
                    statement = sc.get("statement") or claim
                    entities = sc.get("entities", [])
                    queries = sc.get("search_queries", [statement])
                    subclaims.append(SubClaim(
                        id=cid,
                        statement=statement,
                        entities=entities,
                        search_queries=queries
                    ))
        except Exception as e:
            logger.warning(f"Sub-claim extraction fallback due to: {e}")

        # Fallback if decomposition produced empty results
        if not subclaims:
            subclaims = [
                SubClaim(
                    id="C1",
                    statement=claim.strip(),
                    entities=[],
                    search_queries=[claim.strip()]
                )
            ]

        state.subclaims = subclaims
        state.agent_logs.append(f"[{self.name}] Decomposed into {len(subclaims)} atomic proposition(s).")

        # 2. Execute live searches across queries via Tavily
        all_raw_results: List[Dict[str, Any]] = []
        seen_urls = set()

        for sc in subclaims:
            for query in sc.search_queries[:2]:
                state.agent_logs.append(f"[{self.name}] Executing Tavily live search: '{query}'")
                search_hits = self.search.search(query, max_results=self.search.max_results)
                for hit in search_hits:
                    url = hit.get("url", "")
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        hit["associated_subclaim_id"] = sc.id
                        all_raw_results.append(hit)

        state.raw_search_results = all_raw_results
        state.agent_logs.append(f"[{self.name}] Retrieved {len(all_raw_results)} verified live web citations via Tavily.")
        return subclaims
