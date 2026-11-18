"""
TruthLens AI - Core Data Models
===============================
Pydantic schemas establishing the typed data contracts between the Orchestrator
and specialized Agents (Research, Evidence, Verification, Report).
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class SubClaim(BaseModel):
    """An atomic, verifiable proposition extracted from a complex claim."""
    id: str = Field(description="Unique identifier, e.g., 'C1', 'C2'")
    statement: str = Field(description="The atomic factual proposition to verify")
    entities: List[str] = Field(default_factory=list, description="Key entities, names, locations, numbers")
    search_queries: List[str] = Field(default_factory=list, description="Targeted web search queries to verify this claim")


class EvidenceItem(BaseModel):
    """A factual citation or excerpt retrieved from live web research."""
    title: str = Field(description="Web page or article title")
    url: str = Field(description="Source URL")
    snippet: str = Field(description="Relevant text excerpt or summary from source")
    domain: str = Field(description="Originating domain name, e.g., 'reuters.com'")
    is_trusted_domain: bool = Field(default=False, description="Flagged true if from high-reputation or academic source")
    stance_tag: Literal["SUPPORTING", "OPPOSING", "CONTEXT"] = Field(
        default="SUPPORTING",
        description="Whether this evidence supports, opposes, or provides background context for the claim"
    )


class SubClaimVerification(BaseModel):
    """The factual assessment of an individual sub-claim against gathered evidence."""
    subclaim_id: str
    subclaim_statement: str
    stance: Literal["SUPPORTS", "REFUTES", "INCONCLUSIVE", "MIXED"] = Field(
        description="Relationship of evidence to the statement"
    )
    confidence_score: float = Field(ge=0.0, le=1.0, description="Confidence level between 0.0 and 1.0")
    reasoning: str = Field(description="Step-by-step reasoning explaining the determination")
    supporting_urls: List[str] = Field(default_factory=list, description="URLs directly corroborating or refuting")


class ConfidenceAssessment(BaseModel):
    """
    Transparent breakdown of confidence factors replacing arbitrary percentages.
    Evaluates source reliability, relevance, agreement, and evidence quantity.
    """
    qualitative_level: Literal["HIGH", "MODERATE", "LOW", "INCONCLUSIVE"] = Field(
        default="MODERATE",
        description="Qualitative assessment level"
    )
    calculated_score: Optional[float] = Field(
        default=0.75,
        ge=0.0,
        le=1.0,
        description="Calibrated score (0.0 to 1.0) derived transparently from multi-factor analysis"
    )
    source_reliability_score: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Authority and reputation factor of originating domains (0.0 to 1.0)"
    )
    source_relevance_score: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Directness with which evidence addresses the core claim (0.0 to 1.0)"
    )
    consensus_agreement_score: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Degree of agreement vs conflict across retrieved sources (0.0 to 1.0)"
    )
    evidence_quantity_score: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Sufficiency and diversity factor of independent evidence items (0.0 to 1.0)"
    )
    score_explanation: str = Field(
        default="",
        description="Transparent justification of how the score/rating was calculated"
    )
    limitations: str = Field(
        default="",
        description="Explicit limitations in available evidence or methodology"
    )


class FactCheckReport(BaseModel):
    """The final comprehensive fact-checking report produced by ReportAgent."""
    claim: str = Field(description="Original user claim investigated")
    verdict: str = Field(description="Overall verdict classification, e.g., 'MIXED / HALF TRUE'")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Overall confidence score (0.0 to 1.0)")
    confidence_assessment: Optional[ConfidenceAssessment] = Field(
        default=None,
        description="Transparent multi-factor confidence breakdown"
    )
    executive_summary: str = Field(description="Concise 2-3 paragraph overview of findings")
    subclaims: List[SubClaim] = Field(default_factory=list, description="Decomposed claims")
    verifications: List[SubClaimVerification] = Field(default_factory=list, description="Per-subclaim analyses")
    evidence_sources: List[EvidenceItem] = Field(default_factory=list, description="All gathered evidence items")
    supporting_evidence: List[EvidenceItem] = Field(default_factory=list, description="Evidence confirming aspects of the claim")
    opposing_evidence: List[EvidenceItem] = Field(default_factory=list, description="Evidence refuting or contradicting aspects")
    context_evidence: List[EvidenceItem] = Field(default_factory=list, description="Background and contextual citations")
    source_reliability_analysis: Optional[str] = Field(default=None, description="Analysis of source credibility and authority")
    historical_nuance_analysis: Optional[str] = Field(default=None, description="Distinction between established facts, interpretations, and folklore")
    potential_biases: Optional[str] = Field(default=None, description="Identified cognitive, political, or reporting bias")
    limitations: Optional[str] = Field(default=None, description="Identified research constraints, data gaps, or caveats")
    references: List[str] = Field(default_factory=list, description="List of source references with URLs")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of analysis")


class FactCheckState(BaseModel):
    """
    Shared working state passed through the sequential agent pipeline:
    User Input -> Research -> Evidence -> Verification -> Report
    """
    raw_claim: str
    context_notes: Optional[str] = None
    subclaims: List[SubClaim] = Field(default_factory=list)
    raw_search_results: List[dict] = Field(default_factory=list)
    evidence: List[EvidenceItem] = Field(default_factory=list)
    verifications: List[SubClaimVerification] = Field(default_factory=list)
    final_report: Optional[FactCheckReport] = None
    agent_logs: List[str] = Field(default_factory=list)
    current_step: str = "INITIALIZED"
