"""
TruthLens AI - Multi-Agent System Package
=========================================
Contains the specialized autonomous agents and the Central Orchestrator:
- ResearchAgent: Deconstructs claims and creates search plans.
- EvidenceAgent: Executes live searches and collects factual citations.
- VerificationAgent: Cross-examines claims against evidence and scores confidence.
- ReportAgent: Compiles executive summaries, verdicts, and exportable reports.
- AgentOrchestrator: Manages state, execution flow, and progress callbacks.
"""

from .research_agent import ResearchAgent
from .evidence_agent import EvidenceAgent
from .verification_agent import VerificationAgent
from .report_agent import ReportAgent
from .orchestrator import AgentOrchestrator

__all__ = [
    "ResearchAgent",
    "EvidenceAgent",
    "VerificationAgent",
    "ReportAgent",
    "AgentOrchestrator",
]
