"""
UI package for TruthLens AI: Styling, themes, and modular components.
"""

from .components import (
    safe_html,
    render_header,
    render_investigation_progress,
    render_workflow_section,
    render_empty_results,
    render_active_query_banner,
    render_verdict_card,
    render_confidence_assessment_card,
    render_executive_summary_card,
    render_subclaims_list,
    render_evidence_list,
    render_separated_evidence_lists,
    render_source_reliability_card,
    render_references_list,
    render_terminal_logs,
)
from .styles import DARK_THEME_CSS, LIGHT_THEME_CSS, get_theme_css

__all__ = [
    "safe_html",
    "render_header",
    "render_investigation_progress",
    "render_workflow_section",
    "render_empty_results",
    "render_active_query_banner",
    "render_verdict_card",
    "render_confidence_assessment_card",
    "render_executive_summary_card",
    "render_subclaims_list",
    "render_evidence_list",
    "render_separated_evidence_lists",
    "render_source_reliability_card",
    "render_references_list",
    "render_terminal_logs",
    "DARK_THEME_CSS",
    "LIGHT_THEME_CSS",
    "get_theme_css",
]
