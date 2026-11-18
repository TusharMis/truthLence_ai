"""
TruthLens AI - UI Stylesheet & Dual-Theme Engine (Black Dark & Light Modes)
==========================================================================
Hackathon-grade visual design:
- Premium 3D typography for TruthLens AI heading (layered depth, specular highlights, realistic lighting)
- Default: Deep Black Cyber Dark Mode (#000000 / #030305, electric purple #A855F7, luminous cyan #22D3EE)
- Dynamic Light Mode (#FFFFFF / #F8FAFC, royal violet #6D28D9, ocean cyan #0891B2, dark readable text)
- 100% adaptive cards, buttons, tabs, inputs, evidence lists, and progress stages.
"""

def get_theme_css(theme: str = "dark") -> str:
    """
    Generates CSS stylesheet dynamically based on active theme ('dark' or 'light').
    Default is deep black dark mode.
    """
    is_dark = (theme.lower() != "light")

    # Palette Configuration
    if is_dark:
        # Dark Cyber Theme
        bg_body = "#030305"
        bg_gradient = "radial-gradient(ellipse at 50% 0%, #150928 0%, #030305 60%, #000000 100%)"
        text_primary = "#F1F5F9"
        text_secondary = "#94A3B8"
        text_muted = "#64748B"
        border_subtle = "#1E1B2E"
        border_highlight = "rgba(168, 85, 247, 0.35)"
        
        card_bg = "rgba(10, 10, 20, 0.85)"
        card_surface = "#080811"
        card_border = "#1E1B2E"
        
        textarea_bg = "#080811"
        textarea_border = "rgba(168, 85, 247, 0.35)"
        textarea_focus_border = "#22D3EE"
        textarea_focus_glow = "0 8px 36px rgba(0, 0, 0, 0.7), 0 0 28px rgba(34, 211, 238, 0.3)"
        
        btn_sec_bg = "#0B0B14"
        btn_sec_border = "#1E1B2E"
        btn_sec_text = "#CBD5E1"
        btn_sec_hover = "#141022"
        btn_sec_hover_border = "#A855F7"
        
        tab_text = "#94A3B8"
        tab_active_text = "#22D3EE"
        tab_active_bg = "rgba(34, 211, 238, 0.08)"
        tab_active_border = "#22D3EE"
        
        title_gradient = "linear-gradient(135deg, #FFFFFF 0%, #F5F3FF 25%, #C084FC 55%, #38BDF8 85%, #22D3EE 100%)"
        title_filters = """
            drop-shadow(0 1px 1px rgba(255, 255, 255, 0.7))
            drop-shadow(0 2px 0 rgba(168, 85, 247, 0.6))
            drop-shadow(0 4px 2px rgba(126, 34, 206, 0.45))
            drop-shadow(0 8px 16px rgba(168, 85, 247, 0.35))
            drop-shadow(0 16px 32px rgba(6, 182, 212, 0.25))
        """
        
        progress_pending_bg = "rgba(10, 10, 18, 0.85)"
        progress_pending_border = "#1A1A28"
        progress_active_border = "#22D3EE"
        progress_active_bg = "linear-gradient(180deg, rgba(6, 182, 212, 0.15) 0%, rgba(10, 10, 20, 0.95) 100%)"
        progress_active_glow = "0 0 20px rgba(34, 211, 238, 0.35)"
        
        terminal_bg = "#040407"
        terminal_border = "#1C192E"
        terminal_text = "#67E8F9"
        
        pill_bg = "rgba(168, 85, 247, 0.1)"
        pill_border = "rgba(168, 85, 247, 0.35)"
        pill_text = "#C084FC"
    else:
        # Crisp Light Theme
        bg_body = "#F8FAFC"
        bg_gradient = "radial-gradient(ellipse at 50% 0%, #EDE9FE 0%, #F8FAFC 55%, #FFFFFF 100%)"
        text_primary = "#0F172A"
        text_secondary = "#475569"
        text_muted = "#64748B"
        border_subtle = "#E2E8F0"
        border_highlight = "rgba(124, 58, 237, 0.3)"
        
        card_bg = "#FFFFFF"
        card_surface = "#FFFFFF"
        card_border = "#E2E8F0"
        
        textarea_bg = "#FFFFFF"
        textarea_border = "#CBD5E1"
        textarea_focus_border = "#0891B2"
        textarea_focus_glow = "0 6px 24px rgba(15, 23, 42, 0.08), 0 0 16px rgba(8, 145, 178, 0.2)"
        
        btn_sec_bg = "#FFFFFF"
        btn_sec_border = "#E2E8F0"
        btn_sec_text = "#334155"
        btn_sec_hover = "#F1F5F9"
        btn_sec_hover_border = "#7C3AED"
        
        tab_text = "#64748B"
        tab_active_text = "#6D28D9"
        tab_active_bg = "rgba(109, 40, 217, 0.08)"
        tab_active_border = "#6D28D9"
        
        title_gradient = "linear-gradient(135deg, #0F172A 0%, #1E1B4B 30%, #581C87 60%, #0369A1 90%)"
        title_filters = """
            drop-shadow(0 1px 0 rgba(255, 255, 255, 0.9))
            drop-shadow(0 2px 1px rgba(147, 51, 234, 0.35))
            drop-shadow(0 4px 6px rgba(15, 23, 42, 0.12))
            drop-shadow(0 10px 24px rgba(124, 58, 237, 0.2))
        """
        
        progress_pending_bg = "#F8FAFC"
        progress_pending_border = "#E2E8F0"
        progress_active_border = "#0891B2"
        progress_active_bg = "linear-gradient(180deg, rgba(8, 145, 178, 0.1) 0%, #FFFFFF 100%)"
        progress_active_glow = "0 4px 16px rgba(8, 145, 178, 0.2)"
        
        terminal_bg = "#0F172A"
        terminal_border = "#1E293B"
        terminal_text = "#38BDF8"
        
        pill_bg = "rgba(109, 40, 217, 0.08)"
        pill_border = "rgba(109, 40, 217, 0.25)"
        pill_text = "#6D28D9"

    css = f"""
<style>
/* Modern Typography Imports */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* Hide Streamlit chrome, toolbars, deploy buttons, and sidebar */
#MainMenu {{ visibility: hidden !important; }}
header {{ visibility: hidden !important; }}
footer {{ visibility: hidden !important; }}
.stDeployButton {{ display: none !important; }}
[data-testid="stToolbar"] {{ display: none !important; }}
[data-testid="stDecoration"] {{ display: none !important; }}
[data-testid="stStatusWidget"] {{ display: none !important; }}
[data-testid="collapsedControl"] {{ display: none !important; }}
[data-testid="stSidebar"] {{ display: none !important; }}
section[data-testid="stSidebar"] {{ display: none !important; }}

/* Base App Body & Canvas */
html, body, [class*="css"], .stApp {{
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: {bg_body} !important;
    color: {text_primary} !important;
    transition: background-color 0.3s ease, color 0.3s ease;
}}

.stApp {{
    background: {bg_gradient} !important;
    min-height: 100vh;
}}

/* Centered layout canvas */
.block-container {{
    max-width: 860px !important;
    padding-top: 1.8rem !important;
    padding-bottom: 4rem !important;
    margin: 0 auto !important;
}}

/* Top Navigation / Utility Bar */
.top-nav-brand {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    font-weight: 700;
    color: {text_secondary};
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.4rem 0.2rem;
}}

.top-nav-brand span {{
    color: #A855F7;
}}

.top-nav-sub {{
    background: {pill_bg};
    color: {pill_text};
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
    font-size: 0.7rem;
    border: 1px solid {pill_border};
    margin-left: 0.3rem;
}}

/* Theme Switcher Button Styling */
button[key="theme_toggle_btn"] {{
    background: {btn_sec_bg} !important;
    border: 1px solid {btn_sec_border} !important;
    color: {btn_sec_text} !important;
    border-radius: 9999px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    padding: 0.35rem 0.9rem !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
    transition: all 0.25s ease !important;
}}

button[key="theme_toggle_btn"]:hover {{
    border-color: {btn_sec_hover_border} !important;
    transform: translateY(-1px) !important;
}}

/* Hero Branding Section */
.hero-container {{
    text-align: center;
    padding: 0.6rem 0 1.2rem 0;
    margin-bottom: 0.8rem;
}}

.hero-pill {{
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.35rem 1rem;
    background: {pill_bg};
    border: 1px solid {pill_border};
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 600;
    color: {pill_text};
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.9rem;
}}

/* PART 1: Premium 3D-Style Typography */
.hero-title {{
    font-size: 3.8rem;
    font-weight: 900;
    letter-spacing: -0.045em;
    line-height: 1.08;
    margin: 0 0 0.65rem 0;
    background: {title_gradient};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: {title_filters};
    transform: perspective(600px) translateZ(0);
    transition: all 0.3s ease;
}}

@media (max-width: 640px) {{
    .hero-title {{
        font-size: 2.7rem;
    }}
}}

.hero-subtitle {{
    font-size: 1.08rem;
    color: {text_secondary};
    max-width: 580px;
    margin: 0 auto;
    line-height: 1.55;
    font-weight: 400;
}}

/* Research Input Textarea Styling */
[data-testid="stTextArea"] textarea {{
    background-color: {textarea_bg} !important;
    border: 1px solid {textarea_border} !important;
    border-radius: 18px !important;
    color: {text_primary} !important;
    font-size: 1.05rem !important;
    line-height: 1.55 !important;
    padding: 1.2rem !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06) !important;
    transition: all 0.25s ease !important;
}}

[data-testid="stTextArea"] textarea:focus {{
    border-color: {textarea_focus_border} !important;
    box-shadow: {textarea_focus_glow} !important;
    outline: none !important;
}}

[data-testid="stTextArea"] textarea::placeholder {{
    color: {text_muted} !important;
    font-size: 0.98rem !important;
}}

/* Primary "Research & Verify" Action Button */
.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, #7C3AED 0%, #9333EA 50%, #0891B2 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(34, 211, 238, 0.4) !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    padding: 0.8rem 1.8rem !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 24px rgba(147, 51, 234, 0.35) !important;
    transition: all 0.25s ease !important;
}}

.stButton > button[kind="primary"]:hover {{
    box-shadow: 0 6px 30px rgba(34, 211, 238, 0.5) !important;
    border-color: #22D3EE !important;
    transform: translateY(-2px) !important;
}}

/* Secondary Action Buttons (Sample pills, reset) */
.stButton > button:not([kind="primary"]):not([key="theme_toggle_btn"]) {{
    background: {btn_sec_bg} !important;
    border: 1px solid {btn_sec_border} !important;
    color: {btn_sec_text} !important;
    border-radius: 9999px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 0.4rem 0.95rem !important;
    transition: all 0.2s ease !important;
}}

.stButton > button:not([kind="primary"]):not([key="theme_toggle_btn"]):hover {{
    border-color: {btn_sec_hover_border} !important;
    color: {text_primary} !important;
    background: {btn_sec_hover} !important;
}}

/* Live Progress Stage Grid */
.progress-stage-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.65rem;
    margin: 1.4rem 0 1.6rem 0;
}}

@media (max-width: 640px) {{
    .progress-stage-grid {{
        grid-template-columns: repeat(2, 1fr);
    }}
}}

.progress-stage-card {{
    background: {progress_pending_bg};
    border: 1px solid {progress_pending_border};
    border-radius: 12px;
    padding: 0.85rem 0.75rem;
    text-align: center;
    backdrop-filter: blur(12px);
    transition: all 0.25s ease;
}}

.progress-stage-card.pending {{
    opacity: 0.65;
}}

.progress-stage-card.active {{
    border-color: {progress_active_border};
    background: {progress_active_bg};
    box-shadow: {progress_active_glow};
    opacity: 1;
}}

.progress-stage-card.completed {{
    border-color: #10B981;
    background: linear-gradient(180deg, rgba(16, 185, 129, 0.12) 0%, {card_surface} 100%);
    opacity: 1;
}}

.progress-stage-icon {{
    font-size: 1.1rem;
    margin-bottom: 0.25rem;
}}

.progress-stage-title {{
    font-size: 0.84rem;
    font-weight: 700;
    color: {text_primary};
    margin-bottom: 0.15rem;
}}

.progress-stage-status {{
    font-size: 0.7rem;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
}}

.status-active-tag {{
    color: #22D3EE;
    animation: pulse 1.8s infinite;
}}

.status-completed-tag {{
    color: #10B981;
}}

.status-pending-tag {{
    color: {text_muted};
}}

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] {{
    gap: 0.5rem;
    border-bottom: 1px solid {border_subtle};
    padding-bottom: 0.2rem;
}}

.stTabs [data-baseweb="tab"] {{
    color: {tab_text} !important;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 0.55rem 1.1rem;
    border-radius: 8px;
    background: transparent;
}}

.stTabs [data-baseweb="tab"]:hover {{
    color: {text_primary} !important;
}}

.stTabs [aria-selected="true"] {{
    color: {tab_active_text} !important;
    background: {tab_active_bg} !important;
    border-bottom: 2px solid {tab_active_border} !important;
}}

/* Empty Results Placeholder Box */
.empty-results-box {{
    background: {card_bg};
    border: 1px dashed {border_highlight};
    border-radius: 14px;
    padding: 2.5rem 1.5rem;
    text-align: center;
    margin: 1rem 0;
}}

/* Generic Semantic Themed Cards */
.claim-banner-card {{
    background: {card_bg};
    border: 1px solid {border_highlight};
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}}

.verdict-container-card {{
    background: {card_surface};
    border: 1px solid {border_highlight};
    border-radius: 14px;
    padding: 1.6rem;
    text-align: center;
    margin: 1.2rem 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}}

.verdict-badge {{
    display: inline-block;
    padding: 0.65rem 1.5rem;
    font-size: 1.18rem;
    font-weight: 800;
    border-radius: 9999px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}}

.verdict-true {{
    background: rgba(34, 211, 238, 0.12);
    color: #0891B2;
    border: 1px solid #06B6D4;
}}

.verdict-false {{
    background: rgba(239, 68, 68, 0.12);
    color: #DC2626;
    border: 1px solid #EF4444;
}}

.verdict-mixed {{
    background: rgba(168, 85, 247, 0.12);
    color: #7C3AED;
    border: 1px solid #A855F7;
}}

.verdict-unverified {{
    background: rgba(100, 116, 139, 0.12);
    color: #64748B;
    border: 1px solid #64748B;
}}

.confidence-card {{
    background: {card_bg};
    border: 1px solid {card_border};
    border-radius: 12px;
    padding: 1.3rem;
    margin-top: 1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}}

.confidence-factor-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.65rem;
    margin: 1rem 0;
}}

@media (max-width: 640px) {{
    .confidence-factor-grid {{
        grid-template-columns: repeat(2, 1fr);
    }}
}}

.confidence-factor-card {{
    background: {progress_pending_bg};
    border: 1px solid {card_border};
    border-radius: 10px;
    padding: 0.8rem;
    text-align: center;
}}

.confidence-factor-title {{
    font-size: 0.72rem;
    color: {text_secondary};
    text-transform: uppercase;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 0.25rem;
}}

.confidence-factor-val {{
    font-size: 1.25rem;
    font-weight: 800;
    color: {tab_active_text};
    font-family: 'JetBrains Mono', monospace;
}}

.confidence-factor-desc {{
    font-size: 0.68rem;
    color: {text_muted};
    margin-top: 0.2rem;
}}

.executive-summary-card {{
    background: {card_bg};
    border: 1px solid {card_border};
    border-radius: 12px;
    padding: 1.4rem;
    margin-top: 1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}}

.subclaim-card {{
    background: {card_bg};
    border: 1px solid {card_border};
    border-radius: 10px;
    padding: 1.2rem;
    margin-bottom: 0.9rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}}

/* Evidence Cards & Stance Accents */
.evidence-card {{
    background: {card_surface};
    border: 1px solid {card_border};
    border-radius: 10px;
    padding: 1.1rem;
    margin-bottom: 0.8rem;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}}

.evidence-card:hover {{
    border-color: {border_highlight};
    transform: translateY(-1px);
}}

.evidence-card.supporting {{
    border-left: 4px solid #0891B2;
}}

.evidence-card.opposing {{
    border-left: 4px solid #EF4444;
}}

.evidence-card.context {{
    border-left: 4px solid #A855F7;
}}

.audit-card {{
    background: {card_bg};
    border: 1px solid {card_border};
    border-radius: 12px;
    padding: 1.3rem;
    margin-top: 1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}}

.ref-item-card {{
    background: {card_bg};
    border: 1px solid {card_border};
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    box-shadow: 0 1px 4px rgba(0,0,0,0.03);
}}

/* Agent Terminal Log Output */
.agent-terminal {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    background: {terminal_bg};
    border: 1px solid {terminal_border};
    border-radius: 10px;
    padding: 1rem;
    color: {terminal_text};
    max-height: 240px;
    overflow-y: auto;
    line-height: 1.6;
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.3);
}}
</style>
"""
    return css


# Pre-generated stylesheets for direct import or backward compatibility
DARK_THEME_CSS = get_theme_css("dark")
LIGHT_THEME_CSS = get_theme_css("light")

__all__ = ["get_theme_css", "DARK_THEME_CSS", "LIGHT_THEME_CSS"]
