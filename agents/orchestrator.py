"""
TruthLens AI - Central Agent Orchestrator
=========================================
Coordinates the sequential execution of the multi-agent fact-checking pipeline:
Research Agent (Tavily live search)
  -> Evidence Agent (Gemini supporting/opposing evidence categorization)
  -> Verification Agent (cross-checking & reasoned verdict)
  -> Report Agent (final evidence-based report with clickable sources)
"""

import logging
from typing import Callable, Optional
from core.models import FactCheckState, FactCheckReport
from core.llm import GeminiClient
from tools.search_tools import SearchEngine
from tools.scraper_tools import WebScraper
from .research_agent import ResearchAgent
from .evidence_agent import EvidenceAgent
from .verification_agent import VerificationAgent
from .report_agent import ReportAgent

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    Central controller that instantiates and orchestrates all specialized agents.
    Passes structured state across the complete investigation sequence without
    exposing technical agent numbering to end users.
    """

    def __init__(
        self,
        gemini_client: Optional[GeminiClient] = None,
        search_engine: Optional[SearchEngine] = None,
        scraper: Optional[WebScraper] = None
    ):
        self.llm = gemini_client or GeminiClient()
        self.search = search_engine or SearchEngine()
        self.scraper = scraper or WebScraper()

        # Instantiate specialized agents
        self.research_agent = ResearchAgent(self.llm, self.search)
        self.evidence_agent = EvidenceAgent(self.llm)
        self.verification_agent = VerificationAgent(self.llm)
        self.report_agent = ReportAgent(self.llm)

    def run_investigation(
        self,
        claim: str,
        progress_callback: Optional[Callable[[str, str], None]] = None
    ) -> FactCheckReport:
        """
        Executes the multi-agent investigation sequence.

        Args:
            claim: User-provided factual statement or news claim.
            progress_callback: Optional hook callback(stage_id, user_friendly_message)
                              to update the Streamlit UI in real-time.

        Returns:
            The finalized FactCheckReport.
        """
        state = FactCheckState(raw_claim=claim)

        def report_step(step_name: str, message: str):
            state.current_step = step_name
            state.agent_logs.append(f"[{step_name}] {message}")
            if progress_callback:
                progress_callback(step_name, message)

        # Stage 1: Researching sources
        report_step("RESEARCH", "Researching sources across the live web...")
        subclaims = self.research_agent.analyze_and_search(claim, state)

        # Stage 2: Analyzing evidence
        report_step("EVIDENCE", "Analyzing evidence for supporting and opposing consensus...")
        evidence = self.evidence_agent.evaluate_evidence(
            claim=claim,
            subclaims=subclaims,
            raw_results=state.raw_search_results,
            state=state
        )

        # Stage 3: Cross-checking facts
        report_step("VERIFICATION", "Cross-checking facts and calculating truth confidence...")
        verifications = self.verification_agent.verify_subclaims(
            subclaims=subclaims,
            evidence=evidence,
            state=state
        )

        # Stage 4: Preparing final report
        report_step("REPORT", "Preparing final evidence-based report...")
        final_report = self.report_agent.generate_report(
            raw_claim=claim,
            subclaims=subclaims,
            evidence=evidence,
            verifications=verifications,
            state=state
        )

        report_step("DONE", f"Investigation complete. Verdict: {final_report.verdict}")
        return final_report
