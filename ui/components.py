"""
TruthLens AI - UI Presentation Components
=========================================
Robust, CommonMark-compliant UI components:
- Guaranteed zero raw HTML leakage via strict whitespace stripping
- Safe HTML rendering with html.escape() for dynamic user/web content
- Native Streamlit multi-column layouts for agent workflow cards
- Evidence cards with Supporting/Opposing stance indicators and clickable links
- Sub-claim verification breakdown cards
"""

import html
from typing import List, Optional
import streamlit as st
from core.models import EvidenceItem, SubClaimVerification, FactCheckReport, ConfidenceAssessment


def safe_html(content: str) -> None:
    """
    Renders trusted application-generated HTML.
    Strips leading and trailing whitespace on every line to guarantee
    CommonMark's 4-space indented code block rule is NEVER triggered.
    """
    clean_lines = [line.strip() for line in content.strip().splitlines() if line.strip()]
    st.markdown("\n".join(clean_lines), unsafe_allow_html=True)


def render_header() -> None:
    """Renders the centered ChatGPT/Perplexity-style hero branding."""
    safe_html(
        """
        <div class="hero-container">
            <div class="hero-pill">
                <span>✦</span> Autonomous Multi-Agent Intelligence • PS03
            </div>
            <h1 class="hero-title">TruthLens AI</h1>
            <p class="hero-subtitle">
                Deconstruct complex claims, search the live web for verified citations,
                and cross-examine facts with multi-agent cognitive reasoning.
            </p>
        </div>
        """
    )


def render_investigation_progress(current_step: str = "IDLE") -> None:
    """
    Renders clean, dynamic progress stages during active research:
    1. Researching sources
    2. Analyzing evidence
    3. Cross-checking facts
    4. Preparing final report
    Avoids technical agent numbering and highlights the active stage.
    """
    if current_step == "IDLE":
        return

    stages = [
        {"id": "RESEARCH", "icon": "🌐", "title": "Researching sources"},
        {"id": "EVIDENCE", "icon": "🔍", "title": "Analyzing evidence"},
        {"id": "VERIFICATION", "icon": "⚖️", "title": "Cross-checking facts"},
        {"id": "REPORT", "icon": "📊", "title": "Preparing final report"},
    ]

    order = {"RESEARCH": 0, "EVIDENCE": 1, "VERIFICATION": 2, "REPORT": 3, "DONE": 4}
    active_idx = order.get(current_step, -1)

    cards_html = []
    for idx, stage in enumerate(stages):
        if current_step == "DONE" or (active_idx >= 0 and idx < active_idx):
            card_class = "progress-stage-card completed"
            icon = "✓"
            status_text = "Completed"
            tag_class = "status-completed-tag"
        elif idx == active_idx:
            card_class = "progress-stage-card active"
            icon = stage["icon"]
            status_text = "In Progress..."
            tag_class = "status-active-tag"
        else:
            card_class = "progress-stage-card pending"
            icon = stage["icon"]
            status_text = "Pending"
            tag_class = "status-pending-tag"

        cards_html.append(
            f'<div class="{card_class}">'
            f'<div class="progress-stage-icon">{icon}</div>'
            f'<div class="progress-stage-title">{html.escape(stage["title"])}</div>'
            f'<div class="progress-stage-status {tag_class}">{status_text}</div>'
            f'</div>'
        )

    grid_html = f'<div class="progress-stage-grid">{"".join(cards_html)}</div>'
    safe_html(grid_html)


def render_workflow_section(active_step: str = "IDLE") -> None:
    """Legacy helper maintained for backward compatibility."""
    render_investigation_progress(active_step)


def render_empty_results() -> None:
    """
    Renders a modern, minimal awaiting-research placeholder.
    Avoids fabricated mock data or fake citations.
    """
    safe_html(
        """
        <div class="empty-results-box">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔍</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #F1F5F9; margin-bottom: 0.35rem;">
                Ready for Research & Verification
            </div>
            <div style="font-size: 0.88rem; color: #94A3B8; max-width: 520px; margin: 0 auto; line-height: 1.5;">
                Enter any factual claim or research query above and click <strong style="color: #22D3EE;">Research & Verify</strong>.
                The 4 specialized agents will autonomously investigate live sources, detect contradictions, and assign a calibrated truth rating.
            </div>
        </div>
        """
    )


def render_active_query_banner(query: str) -> None:
    """Renders the styled banner displaying the active query being investigated."""
    esc_query = html.escape(str(query).strip())
    safe_html(
        f"""
        <div class="claim-banner-card">
            <div style="font-size: 0.78rem; color: #C084FC; text-transform: uppercase; font-weight: 700; letter-spacing: 0.06em; font-family: 'JetBrains Mono', monospace;">
                Investigated Claim Statement
            </div>
            <div style="font-size: 1.08rem; font-weight: 600; margin-top: 0.35rem; line-height: 1.45;">
                "{esc_query}"
            </div>
        </div>
        """
    )


def render_verdict_card(
    verdict: str,
    confidence_score: float,
    qualitative_level: Optional[str] = None
) -> None:
    """Renders the official verdict hero badge and qualitative confidence level."""
    verdict_clean = html.escape(str(verdict).strip())
    verdict_upper = verdict_clean.upper()

    if "TRUE" in verdict_upper and "MOSTLY" not in verdict_upper and "HALF" not in verdict_upper:
        badge_class = "verdict-true"
    elif "FALSE" in verdict_upper or "DEBUNKED" in verdict_upper:
        badge_class = "verdict-false"
    elif "MIXED" in verdict_upper or "HALF" in verdict_upper or "MOSTLY" in verdict_upper:
        badge_class = "verdict-mixed"
    else:
        badge_class = "verdict-unverified"

    qual_str = html.escape(qualitative_level.upper()) if qualitative_level else "MODERATE"
    conf_pct = int(confidence_score * 100) if confidence_score is not None else 50

    safe_html(
        f"""
        <div class="verdict-container-card">
            <div style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem; font-family: 'JetBrains Mono', monospace; opacity: 0.85;">
                TruthLens Official Verdict
            </div>
            <div class="verdict-badge {badge_class}">
                {verdict_clean}
            </div>
            <div style="margin-top: 1rem; font-size: 0.95rem; display: flex; align-items: center; justify-content: center; gap: 0.8rem; flex-wrap: wrap;">
                <span>Confidence Assessment: <strong style="color: #22D3EE; font-size: 1.05rem;">{conf_pct}%</strong></span>
                <span style="background: rgba(168, 85, 247, 0.15); color: #C084FC; border: 1px solid rgba(168, 85, 247, 0.4); padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.78rem; font-weight: 700; font-family: 'JetBrains Mono', monospace;">
                    {qual_str} CONFIDENCE
                </span>
            </div>
        </div>
        """
    )


def render_confidence_assessment_card(
    assessment: Optional[ConfidenceAssessment],
    confidence_score: float
) -> None:
    """
    Renders transparent multi-factor confidence breakdown instead of arbitrary percentages.
    Includes source reliability, relevance, agreement, and evidence quantity factors.
    """
    if not assessment:
        conf_pct = int(confidence_score * 100)
        safe_html(
            f"""
            <div class="confidence-card">
                <div style="font-size: 0.82rem; font-weight: 700; color: #22D3EE; text-transform: uppercase; letter-spacing: 0.05em; font-family: 'JetBrains Mono', monospace;">
                    ⚖️ Multi-Factor Confidence Assessment
                </div>
                <div style="margin-top: 0.5rem; font-size: 0.9rem;">
                    Calibrated metric: <strong style="color: #22D3EE;">{conf_pct}%</strong>
                </div>
            </div>
            """
        )
        return

    qual_level = html.escape(assessment.qualitative_level.upper())
    rel_pct = int(assessment.source_reliability_score * 100)
    rev_pct = int(assessment.source_relevance_score * 100)
    agr_pct = int(assessment.consensus_agreement_score * 100)
    qty_pct = int(assessment.evidence_quantity_score * 100)
    score_pct = int(assessment.calculated_score * 100) if assessment.calculated_score is not None else int(confidence_score * 100)

    esc_explanation = html.escape(assessment.score_explanation)
    esc_limitations = html.escape(assessment.limitations)

    safe_html(
        f"""
        <div class="confidence-card">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; margin-bottom: 0.6rem;">
                <div style="font-size: 0.82rem; font-weight: 700; color: #22D3EE; text-transform: uppercase; letter-spacing: 0.05em; font-family: 'JetBrains Mono', monospace;">
                    ⚖️ Transparent Confidence Assessment
                </div>
                <div style="background: rgba(34, 211, 238, 0.12); color: #22D3EE; border: 1px solid rgba(34, 211, 238, 0.35); padding: 0.2rem 0.6rem; border-radius: 6px; font-size: 0.75rem; font-weight: 700; font-family: 'JetBrains Mono', monospace;">
                    {qual_level} ({score_pct}%)
                </div>
            </div>
            
            <p style="font-size: 0.84rem; opacity: 0.85; margin-bottom: 0.8rem; line-height: 1.45;">
                Confidence is calculated mathematically from four independent factors rather than an arbitrary figure:
            </p>

            <div class="confidence-factor-grid">
                <div class="confidence-factor-card">
                    <div class="confidence-factor-title">🛡️ Source Reliability</div>
                    <div class="confidence-factor-val">{rel_pct}%</div>
                    <div class="confidence-factor-desc">Academic, gov & reputable media</div>
                </div>
                <div class="confidence-factor-card">
                    <div class="confidence-factor-title">🎯 Source Relevance</div>
                    <div class="confidence-factor-val">{rev_pct}%</div>
                    <div class="confidence-factor-desc">Direct correspondence to claim</div>
                </div>
                <div class="confidence-factor-card">
                    <div class="confidence-factor-title">🤝 Consensus Agreement</div>
                    <div class="confidence-factor-val">{agr_pct}%</div>
                    <div class="confidence-factor-desc">Cross-source consistency</div>
                </div>
                <div class="confidence-factor-card">
                    <div class="confidence-factor-title">📚 Evidence Quantity</div>
                    <div class="confidence-factor-val">{qty_pct}%</div>
                    <div class="confidence-factor-desc">Sample size & diversity</div>
                </div>
            </div>

            <div style="font-size: 0.84rem; line-height: 1.5; margin-top: 0.6rem;">
                <strong style="color: #C084FC;">Calculation Justification:</strong> {esc_explanation}
            </div>

            <div style="font-size: 0.82rem; opacity: 0.8; line-height: 1.45; margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid rgba(128,128,128,0.15);">
                <strong style="color: #8B5CF6;">Identified Limitations:</strong> {esc_limitations}
            </div>
        </div>
        """
    )


def render_executive_summary_card(
    summary: str,
    historical_nuance: Optional[str] = None,
    biases: Optional[str] = None,
    limitations: Optional[str] = None
) -> None:
    """Renders the executive summary with dedicated historical nuance, bias, and limitation sections."""
    esc_summary = html.escape(summary).replace("\n\n", "<br><br>").replace("\n", "<br>")
    
    historical_html = ""
    if historical_nuance:
        esc_hist = html.escape(historical_nuance).replace("\n\n", "<br><br>").replace("\n", "<br>")
        historical_html = f"""
        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(34, 211, 238, 0.2); font-size: 0.88rem;">
            <div style="font-weight: 700; color: #22D3EE; margin-bottom: 0.35rem; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; text-transform: uppercase;">
                🏛️ Established Facts vs. Historical Folklore & Propaganda
            </div>
            <div style="line-height: 1.6; opacity: 0.95;">{esc_hist}</div>
        </div>
        """

    bias_html = ""
    if biases:
        esc_bias = html.escape(biases)
        bias_html = f"""
        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(168, 85, 247, 0.2); font-size: 0.85rem;">
            <strong style="color: #C084FC;">⚡ Potential Bias & Sensationalism Analysis:</strong>
            <p style="margin-top: 0.3rem; opacity: 0.85; line-height: 1.5;">{esc_bias}</p>
        </div>
        """

    limitations_html = ""
    if limitations:
        esc_limit = html.escape(limitations)
        limitations_html = f"""
        <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(128, 128, 128, 0.15); font-size: 0.82rem; opacity: 0.85;">
            <strong style="color: #8B5CF6;">⚠️ Research Scope & Evidence Limitations:</strong>
            <p style="margin-top: 0.25rem; line-height: 1.45;">{esc_limit}</p>
        </div>
        """

    safe_html(
        f"""
        <div class="executive-summary-card">
            <div style="font-size: 0.8rem; font-weight: 700; color: #22D3EE; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.6rem; font-family: 'JetBrains Mono', monospace;">
                Executive Findings Summary
            </div>
            <div style="font-size: 0.95rem; line-height: 1.65; opacity: 0.95;">
                {esc_summary}
            </div>
            {historical_html}
            {bias_html}
            {limitations_html}
        </div>
        """
    )


def render_subclaims_list(verifications: List[SubClaimVerification]) -> None:
    """Renders atomic sub-claims with their individual stance badges and forensic reasoning."""
    if not verifications:
        st.info("No sub-claim verifications recorded.")
        return

    for v in verifications:
        esc_statement = html.escape(v.subclaim_statement)
        esc_reasoning = html.escape(v.reasoning)
        stance = v.stance.upper()
        
        if stance == "SUPPORTS":
            stance_badge = '<span style="background: rgba(34, 211, 238, 0.15); color: #0891B2; border: 1px solid #06B6D4; padding: 0.2rem 0.6rem; border-radius: 6px; font-weight: 700; font-size: 0.75rem;">✓ SUPPORTS</span>'
        elif stance == "REFUTES":
            stance_badge = '<span style="background: rgba(239, 68, 68, 0.15); color: #DC2626; border: 1px solid #EF4444; padding: 0.2rem 0.6rem; border-radius: 6px; font-weight: 700; font-size: 0.75rem;">✗ REFUTES</span>'
        elif stance == "MIXED":
            stance_badge = '<span style="background: rgba(168, 85, 247, 0.15); color: #7C3AED; border: 1px solid #A855F7; padding: 0.2rem 0.6rem; border-radius: 6px; font-weight: 700; font-size: 0.75rem;">~ MIXED</span>'
        else:
            stance_badge = '<span style="background: rgba(100, 116, 139, 0.15); color: #64748B; border: 1px solid #64748B; padding: 0.2rem 0.6rem; border-radius: 6px; font-weight: 700; font-size: 0.75rem;">? INCONCLUSIVE</span>'

        conf_pct = int(v.confidence_score * 100)

        urls_html = ""
        if v.supporting_urls:
            url_links = []
            for u in v.supporting_urls[:3]:
                url_links.append(f'<a href="{html.escape(u)}" target="_blank" style="color: #06B6D4; text-decoration: underline; margin-right: 0.8rem;">{html.escape(u[:45])}...</a>')
            urls_html = f'<div style="font-size: 0.78rem; margin-top: 0.6rem; opacity: 0.75;">Corroborating citations: {" ".join(url_links)}</div>'

        safe_html(
            f"""
            <div class="subclaim-card">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="font-size: 0.75rem; font-family: 'JetBrains Mono', monospace; color: #C084FC; font-weight: 700;">PROPOSITION {html.escape(v.subclaim_id)}</span>
                    <div>
                        {stance_badge}
                        <span style="font-size: 0.78rem; opacity: 0.8; margin-left: 0.6rem; font-family: 'JetBrains Mono', monospace;">Confidence: {conf_pct}%</span>
                    </div>
                </div>
                <div style="font-weight: 600; font-size: 0.98rem; margin-bottom: 0.5rem; line-height: 1.4;">
                    "{esc_statement}"
                </div>
                <div style="font-size: 0.85rem; opacity: 0.9; line-height: 1.5; background: rgba(128,128,128,0.08); padding: 0.7rem; border-radius: 8px;">
                    <strong>Reasoning:</strong> {esc_reasoning}
                </div>
                {urls_html}
            </div>
            """
        )


def render_separated_evidence_lists(
    supporting_items: List[EvidenceItem],
    opposing_items: List[EvidenceItem],
    context_items: Optional[List[EvidenceItem]] = None
) -> None:
    """
    Renders supporting and opposing evidence separately with full source traceability:
    original titles, domains, and clickable links. Never displays fabricated citations.
    """
    context_items = context_items or []

    def render_items_group(items: List[EvidenceItem], stance_type: str, title_str: str, color_hex: str):
        safe_html(
            f"""
            <div style="margin-top: 1.2rem; margin-bottom: 0.6rem; display: flex; align-items: center; justify-content: space-between;">
                <div style="font-weight: 700; color: {color_hex}; font-size: 0.92rem; font-family: 'JetBrains Mono', monospace; text-transform: uppercase;">
                    {title_str} ({len(items)})
                </div>
            </div>
            """
        )
        if not items:
            st.info(f"No {stance_type.lower()} citations recorded in retrieved web intelligence.")
            return

        for item in items:
            esc_title = html.escape(str(item.title))
            esc_url = html.escape(str(item.url))
            esc_domain = html.escape(str(item.domain))
            esc_snippet = html.escape(str(item.snippet))
            
            trust_tag = '<span style="color: #0891B2; font-weight: 700;">[Verified Domain]</span> ' if item.is_trusted_domain else ''
            
            card_class = f"evidence-card {stance_type.lower()}"

            safe_html(
                f"""
                <div class="{card_class}">
                    <div style="font-weight: 600; font-size: 0.98rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;">
                        <div>
                            {trust_tag}<a href="{esc_url}" target="_blank" style="color: #7C3AED; text-decoration: none;">{esc_title} ↗</a>
                        </div>
                    </div>
                    <div style="font-size: 0.78rem; opacity: 0.75; margin: 0.35rem 0; font-family: 'JetBrains Mono', monospace;">
                        Domain: <span>{esc_domain}</span> | Link: <a href="{esc_url}" target="_blank" style="color: #0891B2; text-decoration: underline;">{esc_url[:55]}...</a>
                    </div>
                    <div style="font-size: 0.86rem; opacity: 0.92; margin-top: 0.4rem; line-height: 1.5;">
                        "{esc_snippet}"
                    </div>
                </div>
                """
            )

    # 1. Supporting Evidence Section
    render_items_group(supporting_items, "SUPPORTING", "🟢 Supporting Evidence", "#0891B2")

    # 2. Opposing Evidence Section
    render_items_group(opposing_items, "OPPOSING", "🔴 Opposing & Refuting Evidence", "#DC2626")

    # 3. Context & Historical Nuance Section
    if context_items:
        render_items_group(context_items, "CONTEXT", "🟣 Background Context & Historical Citations", "#7C3AED")


def render_source_reliability_card(
    source_analysis: Optional[str],
    evidence: List[EvidenceItem]
) -> None:
    """Renders comprehensive breakdown of domain credibility and source authority."""
    total = len(evidence)
    trusted_count = sum(1 for e in evidence if e.is_trusted_domain)
    trusted_pct = int((trusted_count / max(1, total)) * 100)

    unique_domains = sorted(list({e.domain for e in evidence if e.domain}))
    domains_html = " • ".join(html.escape(d) for d in unique_domains[:10])

    analysis_text = source_analysis or (
        f"Evaluated {total} independent live citations across {len(unique_domains)} domains. "
        f"{trusted_pct}% of sources originate from high-credibility academic, governmental, or verified media publishers."
    )
    esc_analysis = html.escape(analysis_text)

    safe_html(
        f"""
        <div class="audit-card">
            <div style="font-size: 0.82rem; font-weight: 700; color: #22D3EE; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.6rem; font-family: 'JetBrains Mono', monospace;">
                🌐 Source Reliability & Domain Credibility Audit
            </div>
            <div style="display: flex; gap: 1.5rem; margin-bottom: 0.8rem; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;">
                <div>Total Sources: <strong>{total}</strong></div>
                <div>Authoritative Domains: <strong style="color: #0891B2;">{trusted_count} ({trusted_pct}%)</strong></div>
            </div>
            <div style="font-size: 0.78rem; opacity: 0.75; margin-bottom: 0.6rem; font-family: 'JetBrains Mono', monospace;">
                Domains Consulted: {domains_html}
            </div>
            <div style="font-size: 0.88rem; line-height: 1.55; opacity: 0.95;">
                {esc_analysis}
            </div>
        </div>
        """
    )


def render_references_list(
    references: List[str],
    evidence: Optional[List[EvidenceItem]] = None
) -> None:
    """Renders clean, transparent, numbered references list with clickable links."""
    safe_html(
        """
        <div style="font-size: 0.82rem; font-weight: 700; color: #22D3EE; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.8rem; font-family: 'JetBrains Mono', monospace;">
            📚 References & Citations Index
        </div>
        """
    )

    items_to_render = evidence if evidence else []
    if not items_to_render and references:
        for idx, ref in enumerate(references, 1):
            safe_html(
                f"""
                <div style="font-size: 0.85rem; margin-bottom: 0.5rem; line-height: 1.45;">
                    <span style="color: #7C3AED; font-family: 'JetBrains Mono', monospace; font-weight: 700;">[{idx}]</span> {html.escape(ref)}
                </div>
                """
            )
        return

    if not items_to_render:
        st.info("No references recorded.")
        return

    for idx, item in enumerate(items_to_render, 1):
        esc_title = html.escape(str(item.title))
        esc_url = html.escape(str(item.url))
        esc_domain = html.escape(str(item.domain))
        
        safe_html(
            f"""
            <div class="ref-item-card">
                <div>
                    <span style="color: #0891B2; font-family: 'JetBrains Mono', monospace; font-weight: 700; margin-right: 0.5rem;">[{idx}]</span>
                    <a href="{esc_url}" target="_blank" style="font-weight: 600; text-decoration: none;">{esc_title} ↗</a>
                </div>
                <div style="font-size: 0.78rem; font-family: 'JetBrains Mono', monospace; opacity: 0.7;">
                    {esc_domain}
                </div>
            </div>
            """
        )


def render_evidence_list(evidence_items: List[EvidenceItem]) -> None:
    """Renders clean citation cards from live web search with Supporting/Opposing stance indicators and clickable links."""
    if not evidence_items:
        st.info("No evidence citations collected yet.")
        return

    for item in evidence_items:
        esc_title = html.escape(str(item.title))
        esc_url = html.escape(str(item.url))
        esc_domain = html.escape(str(item.domain))
        esc_snippet = html.escape(str(item.snippet))
        
        trust_tag = '<span style="color: #22D3EE; font-weight: 700;">[Verified Domain]</span> ' if item.is_trusted_domain else ''
        
        stance_str = getattr(item, "stance_tag", "SUPPORTING").upper()
        if stance_str == "SUPPORTING":
            stance_pill = '<span style="background: rgba(34, 211, 238, 0.12); color: #22D3EE; border: 1px solid rgba(34, 211, 238, 0.35); font-size: 0.7rem; font-weight: 700; padding: 0.15rem 0.5rem; border-radius: 4px; margin-left: 0.5rem;">SUPPORTING</span>'
        elif stance_str == "OPPOSING":
            stance_pill = '<span style="background: rgba(239, 68, 68, 0.12); color: #F87171; border: 1px solid rgba(239, 68, 68, 0.35); font-size: 0.7rem; font-weight: 700; padding: 0.15rem 0.5rem; border-radius: 4px; margin-left: 0.5rem;">OPPOSING</span>'
        else:
            stance_pill = '<span style="background: rgba(168, 85, 247, 0.12); color: #C084FC; border: 1px solid rgba(168, 85, 247, 0.35); font-size: 0.7rem; font-weight: 700; padding: 0.15rem 0.5rem; border-radius: 4px; margin-left: 0.5rem;">CONTEXT</span>'

        safe_html(
            f"""
            <div class="evidence-card">
                <div style="font-weight: 600; font-size: 0.98rem; color: #F1F5F9; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;">
                    <div>
                        {trust_tag}<a href="{esc_url}" target="_blank" style="color: #C084FC; text-decoration: none;">{esc_title} ↗</a>
                    </div>
                    <div>{stance_pill}</div>
                </div>
                <div style="font-size: 0.78rem; color: #64748B; margin: 0.3rem 0; font-family: 'JetBrains Mono', monospace;">
                    Domain: <span style="color: #94A3B8;">{esc_domain}</span> | Link: <a href="{esc_url}" target="_blank" style="color: #67E8F9; text-decoration: underline;">{esc_url[:55]}...</a>
                </div>
                <div style="font-size: 0.85rem; color: #CBD5E1; margin-top: 0.4rem; line-height: 1.5;">
                    "{esc_snippet}"
                </div>
            </div>
            """
        )


def render_terminal_logs(logs: List[str]) -> None:
    """Renders real-time agent execution stream in a dark terminal widget."""
    if not logs:
        escaped_logs = "Awaiting pipeline invocation..."
    else:
        escaped_logs = "<br>".join(html.escape(str(line)) for line in logs)

    safe_html(f'<div class="agent-terminal">{escaped_logs}</div>')


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
]
