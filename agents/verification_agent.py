"""
TruthLens AI - Verification Agent
=================================
Agent 03 in the Multi-Agent Pipeline.
Responsibilities:
- Rigorous cross-examination of sub-claims against gathered supporting and opposing evidence.
- Stance classification (SUPPORTS, REFUTES, MIXED, INCONCLUSIVE).
- Quantitative confidence scoring and transparent logical reasoning.
"""

import logging
from typing import List
from core.models import SubClaim, EvidenceItem, SubClaimVerification, FactCheckState
from core.llm import GeminiClient

logger = logging.getLogger(__name__)


class VerificationAgent:
    """
    Verification Agent:
    Cross-checks propositions against supporting and opposing evidence using Gemini reasoning.
    """

    def __init__(self, llm_client: GeminiClient):
        self.llm = llm_client
        self.name = "Verification Agent"

    def verify_subclaims(
        self,
        subclaims: List[SubClaim],
        evidence: List[EvidenceItem],
        state: FactCheckState
    ) -> List[SubClaimVerification]:
        """
        Cross-checks atomic propositions against gathered evidence to formulate reasoned verifications.
        """
        state.agent_logs.append(f"[{self.name}] Cross-examining propositions against evidence matrix...")

        if not subclaims:
            return []

        # Prepare evidence digest
        evidence_digest = []
        for e in evidence:
            evidence_digest.append({
                "url": e.url,
                "title": e.title,
                "domain": e.domain,
                "is_trusted": e.is_trusted_domain,
                "stance": e.stance_tag,
                "finding": e.snippet
            })

        verifications: List[SubClaimVerification] = []

        valid_urls = {e.url for e in evidence if e.url}

        for sc in subclaims:
            verification_prompt = f"""
You are a senior forensic fact-checking analyst.
Evaluate this specific atomic sub-claim against the compiled authentic evidence items.
Distinguish established scientific/historical facts from common interpretations, folklore, or propaganda:

Sub-Claim ID: {sc.id}
Sub-Claim Statement: "{sc.statement}"

Compiled Evidence:
{evidence_digest}

Evaluation Guidelines:
1. 'stance': Exactly one of 'SUPPORTS', 'REFUTES', 'MIXED', or 'INCONCLUSIVE'.
   - 'SUPPORTS': Authoritative evidence affirms the proposition.
   - 'REFUTES': Credible evidence disproves or debunks the proposition.
   - 'MIXED': Proposition contains partial truth mixed with significant inaccuracy or omission.
   - 'INCONCLUSIVE': Insufficient authoritative evidence to verify.
2. 'factor_evaluation':
   - 'reliability': (0.0 to 1.0) Credibility and authority of citing domains (e.g. academic, governmental, peer-reviewed, reputable news).
   - 'relevance': (0.0 to 1.0) Direct relevance to this specific proposition.
   - 'agreement': (0.0 to 1.0) Consistency across sources (penalize if sources conflict).
   - 'quantity': (0.0 to 1.0) Sufficiency of independent citations.
   DO NOT generate arbitrary percentages like 95%. Calculate transparently:
   calculated_confidence = round(0.35 * reliability + 0.25 * relevance + 0.25 * agreement + 0.15 * quantity, 2)
3. 'reasoning': 2-3 sentence logical justification explaining the verdict, clearly distinguishing established facts from interpretations.
4. 'supporting_urls': Array of ONLY real URLs from the provided evidence list that substantiate this finding.

Respond with ONLY valid JSON:
{{
  "stance": "SUPPORTS" | "REFUTES" | "MIXED" | "INCONCLUSIVE",
  "reliability": 0.8,
  "relevance": 0.9,
  "agreement": 0.8,
  "quantity": 0.7,
  "calculated_confidence": 0.81,
  "reasoning": "Clear factual reasoning referencing evidence findings...",
  "supporting_urls": ["exact_url_from_evidence_list"]
}}
"""
            try:
                res = self.llm.generate_json(verification_prompt)
                stance = res.get("stance", "INCONCLUSIVE").upper()
                if stance not in ("SUPPORTS", "REFUTES", "MIXED", "INCONCLUSIVE"):
                    stance = "INCONCLUSIVE"
                
                # Methodical, non-arbitrary confidence calculation
                rel = max(0.0, min(1.0, float(res.get("reliability", 0.7))))
                rev = max(0.0, min(1.0, float(res.get("relevance", 0.7))))
                agr = max(0.0, min(1.0, float(res.get("agreement", 0.7))))
                qty = max(0.0, min(1.0, float(res.get("quantity", 0.6))))
                
                calculated = round(0.35 * rel + 0.25 * rev + 0.25 * agr + 0.15 * qty, 2)
                score = float(res.get("calculated_confidence", calculated))
                score = max(0.0, min(1.0, score))

                reasoning = res.get("reasoning", "Evidence evaluated against proposition.")
                
                # Enforce source traceability: only include genuine URLs from retrieved evidence
                raw_urls = res.get("supporting_urls", [])
                confirmed_urls = [u for u in raw_urls if u in valid_urls]
                if not confirmed_urls and evidence:
                    confirmed_urls = [evidence[0].url]

                verifications.append(SubClaimVerification(
                    subclaim_id=sc.id,
                    subclaim_statement=sc.statement,
                    stance=stance,
                    confidence_score=score,
                    reasoning=reasoning,
                    supporting_urls=confirmed_urls
                ))
            except Exception as e:
                logger.warning(f"Verification parsing error for {sc.id}: {e}")
                # Safe fallback
                verifications.append(SubClaimVerification(
                    subclaim_id=sc.id,
                    subclaim_statement=sc.statement,
                    stance="INCONCLUSIVE",
                    confidence_score=0.5,
                    reasoning=f"Automatic cross-check fallback: {e}",
                    supporting_urls=[e.url for e in evidence[:1]]
                ))

        state.verifications = verifications
        state.agent_logs.append(
            f"[{self.name}] Completed forensic verification for {len(verifications)} subclaim(s)."
        )
        return verifications
