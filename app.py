"""
TruthLens AI - Main Application
===============================
Problem Statement PS03: Autonomous Multi-Agent Research & Fact-Checking System
Modern ChatGPT / Perplexity-style AI product:
- Centered, distraction-free layout (technical sidebar completely removed)
- Prominent TruthLens AI hero branding
- Large research query input with sample suggestions
- "✦ Research & Verify" primary action button connected to live 4-agent orchestrator
- Real live Tavily Web Research & Google Gemini reasoning
- Visible 4-agent workflow cards (st.columns layout, 100% code-leak free)
- Clickable evidence sources matrix & comprehensive truth rating
- Secure configuration via .env locally and st.secrets on Streamlit Cloud
"""

import streamlit as st
from config import settings
from ui.styles import get_theme_css, DARK_THEME_CSS, LIGHT_THEME_CSS
from ui.components import (
    safe_html,
    render_header,
    render_investigation_progress,
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
from agents.orchestrator import AgentOrchestrator

# 1. Page Configuration: Centered layout, collapsed sidebar
st.set_page_config(
    page_title="TruthLens AI | Multi-Agent Fact-Checking",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)


def init_session_state():
    """Initializes session state variables for clean UI reactivity and theme persistence."""
    if "theme" not in st.session_state:
        # Default: Professional Black Dark Mode; persist via query parameters if provided
        url_theme = st.query_params.get("theme", "dark")
        st.session_state.theme = "light" if url_theme == "light" else "dark"
    if "logs" not in st.session_state:
        st.session_state.logs = []
    if "current_step" not in st.session_state:
        st.session_state.current_step = "IDLE"
    if "analysis_triggered" not in st.session_state:
        st.session_state.analysis_triggered = False
    if "report" not in st.session_state:
        st.session_state.report = None
    if "last_query" not in st.session_state:
        st.session_state.last_query = ""
    if "query_input_text" not in st.session_state:
        st.session_state.query_input_text = ""


def validate_input(query: str) -> tuple[bool, str]:
    """
    Validates user query input.
    Returns (is_valid, error_message).
    """
    clean = query.strip()
    if not clean:
        return False, "Please enter a research question or factual statement to verify."
    if len(clean) < 10:
        return False, "The query is too short. Please provide at least 10 characters for substantive research."
    if len(clean.split()) < 3:
        return False, "Please enter at least 3 words to allow meaningful claim extraction."
    return True, ""


def main():
    """Main application loop."""
    init_session_state()

    # 2. Inject Active Theme CSS (Default: Black Dark Mode; persists dynamically)
    active_theme = st.session_state.get("theme", "dark")
    st.markdown(get_theme_css(active_theme), unsafe_allow_html=True)

    # 3. Top Utility Navigation: Brand tag & Top-Right Dark/Light Mode Toggle
    col_nav_left, col_nav_right = st.columns([5.2, 1.8])
    with col_nav_left:
        safe_html(
            '<div class="top-nav-brand"><span>✦</span> TruthLens AI <span class="top-nav-sub">PS03 • MULTI-AGENT</span></div>'
        )
    with col_nav_right:
        is_dark = (active_theme == "dark")
        toggle_label = "☀️ Light Mode" if is_dark else "🌙 Dark Mode"
        if st.button(toggle_label, key="theme_toggle_btn", use_container_width=True):
            new_theme = "light" if is_dark else "dark"
            st.session_state.theme = new_theme
            st.query_params["theme"] = new_theme
            st.rerun()

    # 4. Centered Hero Branding (3D-style typography with layered depth & lighting)
    render_header()

    # 2. Large Perplexity/ChatGPT-Style Research Input Box
    query_text = st.text_area(
        label="Research question or claim",
        value=st.session_state.query_input_text,
        placeholder="Ask any research question or paste a claim to verify with live web sources...\n(e.g., 'NASA confirmed the discovery of living plant organisms on Mars in 2026.')",
        height=110,
        label_visibility="collapsed",
        key="main_query_area"
    )

    # 3. Quick Sample Suggestion Pills
    safe_html('<div style="font-size: 0.8rem; color: #94A3B8; font-weight: 500; margin: 0.6rem 0 0.4rem 0;">💡 Try an example:</div>')
    
    col_p1, col_p2, col_p3 = st.columns(3)
    sample_1 = "NASA confirmed the discovery of living plant organisms on Mars in 2026."
    sample_2 = "Eating carrots significantly improves human night vision."
    sample_3 = "Natural raw honey never spoils even after thousands of years."

    with col_p1:
        if st.button("🌱 Plants on Mars", use_container_width=True):
            st.session_state.query_input_text = sample_1
            st.session_state.report = None
            st.rerun()

    with col_p2:
        if st.button("🥕 Carrots & Vision", use_container_width=True):
            st.session_state.query_input_text = sample_2
            st.session_state.report = None
            st.rerun()

    with col_p3:
        if st.button("🍯 Honey Spoilage", use_container_width=True):
            st.session_state.query_input_text = sample_3
            st.session_state.report = None
            st.rerun()

    # 4. Action Buttons: "Research & Verify" & "Reset"
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    col_act1, col_act2 = st.columns([3, 1])

    with col_act1:
        verify_clicked = st.button(
            "✦ Research & Verify",
            use_container_width=True,
            type="primary"
        )

    with col_act2:
        reset_clicked = st.button("🔄 Reset", use_container_width=True)

    if reset_clicked:
        st.session_state.logs = []
        st.session_state.current_step = "IDLE"
        st.session_state.analysis_triggered = False
        st.session_state.report = None
        st.session_state.last_query = ""
        st.session_state.query_input_text = ""
        st.rerun()

    # 5. Dynamic Live Progress Tracker (Active only during/after research execution)
    progress_placeholder = st.empty()
    if st.session_state.current_step != "IDLE":
        with progress_placeholder.container():
            render_investigation_progress(st.session_state.current_step)

    # 6. Action Execution, Input Validation & Real Multi-Agent Orchestration
    if verify_clicked:
        active_query = query_text if query_text else st.session_state.query_input_text
        is_valid, validation_msg = validate_input(active_query)

        if not is_valid:
            st.error(f"⚠️ **Input Required:** {validation_msg}")
        elif not settings.is_gemini_connected:
            # Graceful error handling without crashing or exposing keys
            st.error(
                "🚫 **Gemini API Not Configured:** `GEMINI_API_KEY` was not found in your environment.\n\n"
                "• **Local Development:** Add `GEMINI_API_KEY=your_key` to your `.env` file in the project root.\n"
                "• **Streamlit Cloud:** Add `GEMINI_API_KEY = \"your_key\"` under **App Settings → Secrets**.\n\n"
                "Get a free Gemini API key at [Google AI Studio](https://aistudio.google.com/app/apikey)."
            )
        else:
            # Inputs & API key verified! Execute real multi-agent investigation
            st.session_state.analysis_triggered = True
            st.session_state.last_query = active_query.strip()
            st.session_state.current_step = "RESEARCH"
            st.session_state.logs = [
                f"[System] Initiated multi-agent investigation: '{active_query.strip()[:65]}...'",
                f"[System] Reasoning Model: {settings.gemini_model} | Search Engine: {settings.search_engine}"
            ]
            with progress_placeholder.container():
                render_investigation_progress("RESEARCH")

            # Display real-time progress container
            with st.status("🔍 Autonomous Multi-Agent Investigation in Progress...", expanded=True) as status_box:
                def progress_handler(step_name: str, detail_message: str):
                    st.session_state.current_step = step_name
                    st.session_state.logs.append(f"[{step_name}] {detail_message}")
                    with progress_placeholder.container():
                        render_investigation_progress(step_name)
                    status_box.write(f"**[{step_name}]** {detail_message}")

                try:
                    orchestrator = AgentOrchestrator()
                    final_report = orchestrator.run_investigation(
                        claim=active_query.strip(),
                        progress_callback=progress_handler
                    )
                    st.session_state.report = final_report
                    st.session_state.current_step = "DONE"
                    with progress_placeholder.container():
                        render_investigation_progress("DONE")
                    
                    conf_display = f"{int(final_report.confidence_score * 100)}%"
                    if final_report.confidence_assessment and final_report.confidence_assessment.qualitative_level:
                        conf_display += f" [{final_report.confidence_assessment.qualitative_level}]"
                    
                    status_box.update(
                        label=f"✅ Fact-Check Complete: {final_report.verdict} ({conf_display} Confidence)",
                        state="complete",
                        expanded=False
                    )
                except Exception as e:
                    st.session_state.current_step = "IDLE"
                    status_box.update(label="❌ Investigation Failed", state="error", expanded=True)
                    st.error(f"An error occurred during multi-agent analysis: {type(e).__name__} - {e}")

    # 7. Readable Research Results & Dossier Tabs (10 Standard Fact-Check Sections)
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown("### 📊 Investigation Results & Evidence Dossier")

    tab_report, tab_evidence, tab_claims, tab_refs, tab_logs = st.tabs([
        "📋 Verified Report",
        "⚖️ Supporting & Opposing Evidence",
        "🔬 Sub-Claims Breakdown",
        "📚 References & Audit",
        "💻 Agent Execution Stream"
    ])

    report = st.session_state.report

    with tab_report:
        if not report:
            render_empty_results()
        else:
            # 1. Investigated Claim
            render_active_query_banner(report.claim)
            
            # 2. Final Verdict
            qual_lvl = report.confidence_assessment.qualitative_level if report.confidence_assessment else None
            render_verdict_card(report.verdict, report.confidence_score, qual_lvl)
            
            # 3. Transparent Confidence Assessment (Multi-factor breakdown)
            render_confidence_assessment_card(report.confidence_assessment, report.confidence_score)
            
            # 4. Executive Summary (with Historical Nuance, Bias Analysis & Limitations)
            render_executive_summary_card(
                summary=report.executive_summary,
                historical_nuance=report.historical_nuance_analysis,
                biases=report.potential_biases,
                limitations=report.limitations
            )
            
            # 5. Source Reliability Analysis
            render_source_reliability_card(report.source_reliability_analysis, report.evidence_sources)

    with tab_evidence:
        if not report:
            render_empty_results()
        else:
            st.markdown("#### Live Web Citations & Stance Categorization")
            st.caption(
                "Evidence retrieved via Tavily Search API and classified by the Evidence Agent. "
                "Supporting and opposing citations are segregated to ensure rigorous neutrality. "
                "Every evidence item retains its original publication title, domain, and clickable link."
            )
            # 6. Supporting & Opposing Evidence (Separated with 100% source traceability)
            render_separated_evidence_lists(
                supporting_items=report.supporting_evidence or [e for e in report.evidence_sources if e.stance_tag == "SUPPORTING"],
                opposing_items=report.opposing_evidence or [e for e in report.evidence_sources if e.stance_tag == "OPPOSING"],
                context_items=report.context_evidence or [e for e in report.evidence_sources if e.stance_tag == "CONTEXT"]
            )

    with tab_claims:
        if not report:
            render_empty_results()
        else:
            st.markdown("#### Atomic Sub-Claims Deconstructed & Cross-Examined")
            st.caption(
                "The Research Agent decomposed the complex claim into atomic propositions. "
                "The Verification Agent cross-referenced each proposition against live evidence to assign calibrated ratings."
            )
            render_subclaims_list(report.verifications)

    with tab_refs:
        if not report:
            render_empty_results()
        else:
            # 7. References Index
            st.caption("Complete, verifiable references index with authentic domain attribution and original source links.")
            render_references_list(
                references=report.references,
                evidence=report.evidence_sources
            )

    with tab_logs:
        st.markdown("#### Multi-Agent Communication & Reasoning Stream")
        render_terminal_logs(st.session_state.logs)


if __name__ == "__main__":
    main()
