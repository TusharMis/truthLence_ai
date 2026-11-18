"""
TruthLens AI - Report Agent
===========================
Agent 04 in the Multi-Agent Pipeline.
Responsibilities:
- Synthesizes all sub-claims, verifications, and categorized evidence.
- Assigns the final calibrated truth rating verdict.
- Drafts an objective, high-clarity Executive Summary.
- Compiles the final transparent FactCheckReport dossier with clickable citations.
"""

import logging
from typing import List
from datetime import datetime
from core.models import (
    SubClaim,
    EvidenceItem,
    SubClaimVerification,
    ConfidenceAssessment,
    FactCheckReport,
    FactCheckState
)
from core.llm import GeminiClient
from config import settings

logger = logging.getLogger(__name__)


class ReportAgent:
    """
    Report Agent:
    Compiles the final transparent, evidence-backed fact-checking dossier,
    multi-factor confidence assessment, and calibrated verdict.
    """

    def __init__(self, llm_client: GeminiClient):
        self.llm = llm_client
        self.name = "Report Agent"

    def generate_report(
        self,
        raw_claim: str,
        subclaims: List[SubClaim],
        evidence: List[EvidenceItem],
        verifications: List[SubClaimVerification],
        state: FactCheckState
    ) -> FactCheckReport:
        """
        Synthesizes the complete fact-checking dossier across the 10 transparent report sections.
        """
        state.agent_logs.append(f"[{self.name}] Synthesizing final fact-checking dossier and consensus verdict...")

        # Separate evidence items by stance for transparent accountability
        supporting_evidence = [e for e in evidence if e.stance_tag == "SUPPORTING"]
        opposing_evidence = [e for e in evidence if e.stance_tag == "OPPOSING"]
        context_evidence = [e for e in evidence if e.stance_tag == "CONTEXT"]

        verifications_summary = []
        for v in verifications:
            verifications_summary.append({
                "subclaim_id": v.subclaim_id,
                "statement": v.subclaim_statement,
                "stance": v.stance,
                "confidence": v.confidence_score,
                "reasoning": v.reasoning
            })

        evidence_summary = []
        for e in evidence:
            evidence_summary.append({
                "title": e.title,
                "domain": e.domain,
                "stance": e.stance_tag,
                "is_trusted": e.is_trusted_domain,
                "url": e.url,
                "excerpt": e.snippet
            })

        # Calculate preliminary baseline heuristics from real sources
        total_sources = len(evidence)
        trusted_count = sum(1 for e in evidence if e.is_trusted_domain)
        source_rel_heuristic = round(min(1.0, (trusted_count / max(1, total_sources)) * 0.75 + 0.25), 2)
        source_qty_heuristic = round(min(1.0, total_sources / 6.0), 2)

        report_prompt = f"""
You are the Chief Fact-Checking Editor for TruthLens AI.
Synthesize the complete multi-agent investigation into an objective, highly transparent final report.

Original Claim Investigated:
"{raw_claim}"

Atomic Sub-Claim Verifications:
{verifications_summary}

Compiled Live Evidence:
{evidence_summary}

Heuristic Baseline:
- Total Sources: {total_sources}
- High-Credibility / Trusted Sources: {trusted_count}
- Baseline Reliability Factor: {source_rel_heuristic}
- Baseline Quantity Factor: {source_qty_heuristic}

Instructions for Factual Rigor & Transparency:
1. 'verdict': Select exactly ONE of:
   - 'VERIFIED TRUE' (Fully corroborated by authoritative consensus)
   - 'MOSTLY TRUE' (Accurate in main substance, minor details slightly off)
   - 'MIXED / HALF TRUE' (Contains both significant truth and falsehoods / myths, e.g. legitimate nutritional benefit vs false claim of superhuman night vision)
   - 'MOSTLY FALSE' (Contains small grain of truth but distorts or omits critical facts)
   - 'DEBUNKED / FALSE' (Factually incorrect, debunked myth, or contradicted by evidence)
   - 'UNVERIFIED / INSUFFICIENT EVIDENCE' (Insufficient reliable data exists)
2. 'confidence_assessment':
   DO NOT generate arbitrary percentages like 95%. Evaluate transparent factors:
   - 'reliability': (0.0 to 1.0) Authority of publishing domains (peer-reviewed, medical/academic, encyclopedic, trusted news).
   - 'relevance': (0.0 to 1.0) Direct correspondence between evidence and the claim.
   - 'agreement': (0.0 to 1.0) Degree of consensus across sources (penalize if sources contradict or leave ambiguity).
   - 'quantity': (0.0 to 1.0) Sufficiency and diversity of independent evidence items.
   - 'qualitative_level': One of 'HIGH', 'MODERATE', 'LOW', or 'INCONCLUSIVE'.
   - 'score_explanation': Clear explanation of how the score/level was determined based on these 4 factors.
   - 'limitations': Explicit statement of research constraints, clinical nuances, or evidence gaps.
3. 'executive_summary': A clear 2-3 paragraph synthesis explaining what the evidence proves or disproves.
4. 'historical_nuance_analysis': Rigorously distinguish established scientific/historical facts from popular interpretations, folklore, or historical propaganda (e.g. WWII British RAF radar deception campaign vs genuine vitamin A physiology).
5. 'source_reliability_analysis': Analysis of the credibility, authority, and distribution of domains analyzed.
6. 'potential_biases': Analysis of sensationalism, cognitive biases, marketing exaggeration, or historical disinformation.
7. 'limitations': Comprehensive disclosure of limitations in evidence, study populations, or scope.

Respond with ONLY valid JSON:
{{
  "verdict": "MIXED / HALF TRUE",
  "reliability": 0.85,
  "relevance": 0.90,
  "agreement": 0.85,
  "quantity": 0.80,
  "qualitative_level": "MODERATE",
  "score_explanation": "Confidence reflects strong domain authority from medical and historical sources, balanced by the distinction between nutritional fact and wartime folklore.",
  "executive_summary": "Two to three well-structured paragraphs summarizing findings...",
  "historical_nuance_analysis": "Detailed breakdown distinguishing established empirical facts from interpretations, folklore, or propaganda...",
  "source_reliability_analysis": "Evaluation of domain credibility and peer-reviewed consensus...",
  "potential_biases": "Identification of cognitive biases, marketing exaggerations, or historical propaganda...",
  "limitations": "Explicit boundaries of evidence, sample populations, or methodology..."
}}
"""
        verdict = "UNVERIFIED / INSUFFICIENT EVIDENCE"
        exec_summary = "Investigation completed across live web sources."
        historical_nuance = None
        source_reliability_desc = None
        biases = None
        limitations = None

        # Defaults for multi-factor confidence assessment
        rel_factor = source_rel_heuristic
        rev_factor = 0.80
        agr_factor = 0.75
        qty_factor = source_qty_heuristic
        qual_level = "MODERATE"
        score_expl = "Confidence computed transparently from multi-factor analysis."
        limit_desc = "Evidence is subject to the scope of retrieved live web citations."

        try:
            report_data = self.llm.generate_json(report_prompt)
            raw_v = report_data.get("verdict", "").strip().upper()
            
            # Map to allowed verdicts
            for valid_v in settings.VERDICTS:
                if valid_v in raw_v or raw_v in valid_v:
                    verdict = valid_v
                    break
            else:
                verdict = raw_v or "UNVERIFIED / INSUFFICIENT EVIDENCE"

            rel_factor = max(0.0, min(1.0, float(report_data.get("reliability", source_rel_heuristic))))
            rev_factor = max(0.0, min(1.0, float(report_data.get("relevance", 0.8))))
            agr_factor = max(0.0, min(1.0, float(report_data.get("agreement", 0.75))))
            qty_factor = max(0.0, min(1.0, float(report_data.get("quantity", source_qty_heuristic))))

            qual_raw = str(report_data.get("qualitative_level", "MODERATE")).upper()
            if qual_raw in ("HIGH", "MODERATE", "LOW", "INCONCLUSIVE"):
                qual_level = qual_raw

            score_expl = report_data.get("score_explanation", score_expl)
            exec_summary = report_data.get("executive_summary", exec_summary)
            historical_nuance = report_data.get("historical_nuance_analysis")
            source_reliability_desc = report_data.get("source_reliability_analysis")
            biases = report_data.get("potential_biases")
            limitations = report_data.get("limitations") or report_data.get("score_explanation")
            limit_desc = limitations or limit_desc

        except Exception as e:
            logger.warning(f"Report synthesis fallback: {e}")
            # Determine basic verdict from subclaims
            refute_count = sum(1 for v in verifications if v.stance == "REFUTES")
            support_count = sum(1 for v in verifications if v.stance == "SUPPORTS")
            if refute_count > 0 and support_count > 0:
                verdict = "MIXED / HALF TRUE"
            elif refute_count > support_count:
                verdict = "DEBUNKED / FALSE"
            elif support_count > refute_count:
                verdict = "VERIFIED TRUE"
            else:
                verdict = "UNVERIFIED / INSUFFICIENT EVIDENCE"

        # Transparently calculate calibrated confidence score
        # Formula: 35% Reliability + 25% Relevance + 25% Consensus Agreement + 15% Quantity
        calculated_score = round(
            (0.35 * rel_factor) + (0.25 * rev_factor) + (0.25 * agr_factor) + (0.15 * qty_factor),
            2
        )

        # Fallback to qualitative confidence if reliable score cannot be calculated
        if total_sources < 2:
            qual_level = "LOW"
            calculated_score = None
            score_expl = "Quantitative confidence score withheld due to sparse citations (< 2 sources). Using qualitative assessment."

        confidence_assessment = ConfidenceAssessment(
            qualitative_level=qual_level,
            calculated_score=calculated_score,
            source_reliability_score=rel_factor,
            source_relevance_score=rev_factor,
            consensus_agreement_score=agr_factor,
            evidence_quantity_score=qty_factor,
            score_explanation=score_expl,
            limitations=limit_desc
        )

        # Build clean, traceable references list
        references = [
            f"{e.title} — {e.domain} ({e.url})"
            for e in evidence if e.url
        ]

        final_report = FactCheckReport(
            claim=raw_claim,
            verdict=verdict,
            confidence_score=calculated_score if calculated_score is not None else 0.5,
            confidence_assessment=confidence_assessment,
            executive_summary=exec_summary,
            subclaims=subclaims,
            verifications=verifications,
            evidence_sources=evidence,
            supporting_evidence=supporting_evidence,
            opposing_evidence=opposing_evidence,
            context_evidence=context_evidence,
            source_reliability_analysis=source_reliability_desc,
            historical_nuance_analysis=historical_nuance,
            potential_biases=biases,
            limitations=limitations,
            references=references,
            created_at=datetime.utcnow()
        )

        state.final_report = final_report
        conf_display = f"{int(calculated_score * 100)}%" if calculated_score is not None else qual_level
        state.agent_logs.append(
            f"[{self.name}] Investigation concluded with verdict: '{verdict}' (Confidence: {conf_display} [{qual_level}])."
        )
        return final_report
