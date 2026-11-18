"""
TruthLens AI - Centralized Configuration Module
===============================================
Single source of truth for all application settings, model selections,
and API credentials.

Security & Resilience Guarantee:
- Loads secrets from backend environment variables via `python-dotenv` (local dev).
- Seamlessly falls back to `st.secrets` when deployed to Streamlit Cloud.
- Dynamically retrieves keys so runtime or .env changes are recognized immediately.
- Provides consistent property AND method accessors (is_gemini_connected / is_gemini_configured).
- Never exposes raw keys in frontend, logs, exceptions, or string representations.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Ensure local .env file is loaded into os.environ
load_dotenv(override=True)


def _get_secret(key: str, default: str = "") -> str:
    """
    Safely retrieves a configuration value or secret.
    Lookup precedence:
    1. Streamlit Cloud Secrets (st.secrets) if running within Streamlit runtime.
    2. Backend environment variables (os.getenv) loaded from .env or system.
    """
    # 1. Attempt retrieval from Streamlit Cloud secrets
    try:
        import streamlit as st
        if hasattr(st, "secrets") and st.secrets is not None:
            if key in st.secrets:
                val = st.secrets[key]
                if val is not None:
                    return str(val).strip()
    except Exception:
        pass

    # 2. Fall back to operating system / .env environment variables
    env_val = os.getenv(key, default)
    return str(env_val).strip() if env_val is not None else default


class Settings:
    """
    Centralized, secure application settings container.
    Protects credentials from being printed or exposed in logs/frontend.
    """

    # Backend credential accessors (used strictly by internal backend clients)
    @property
    def gemini_api_key(self) -> str:
        """Raw Gemini API key for backend LLM clients only."""
        return _get_secret("GEMINI_API_KEY", "")

    @property
    def tavily_api_key(self) -> str:
        """Raw Tavily API key for backend search tools only."""
        return _get_secret("TAVILY_API_KEY", "")

    # Public runtime parameters
    @property
    def gemini_model(self) -> str:
        return _get_secret("GEMINI_MODEL", "gemini-3.1-flash-lite")

    @property
    def search_engine(self) -> str:
        return _get_secret("SEARCH_ENGINE", "tavily").lower()

    @property
    def max_search_results(self) -> int:
        try:
            return int(_get_secret("MAX_SEARCH_RESULTS", "5"))
        except (ValueError, TypeError):
            return 5

    @property
    def debug_mode(self) -> bool:
        return _get_secret("DEBUG_MODE", "False").lower() in ("true", "1")

    @property
    def log_level(self) -> str:
        return _get_secret("LOG_LEVEL", "INFO")

    # Safe public connection status checks (Consistent properties AND methods)
    @property
    def is_gemini_connected(self) -> bool:
        """Returns True if a valid Gemini API key is configured."""
        key = self.gemini_api_key
        if not key:
            return False
        if "your_gemini_api_key" in key.lower():
            return False
        return len(key) >= 15

    def is_gemini_configured(self, runtime_key: Optional[str] = None) -> bool:
        """Backward-compatible method accessor for Gemini status check."""
        if runtime_key and runtime_key.strip():
            k = runtime_key.strip()
            return len(k) >= 15 and "your_gemini_api_key" not in k.lower()
        return self.is_gemini_connected

    @property
    def is_tavily_connected(self) -> bool:
        """Returns True if a valid Tavily API key is configured."""
        key = self.tavily_api_key
        if not key:
            return False
        if "your_tavily_api_key" in key.lower():
            return False
        return len(key) >= 10

    def is_tavily_configured(self, runtime_key: Optional[str] = None) -> bool:
        """Backward-compatible method accessor for Tavily status check."""
        if runtime_key and runtime_key.strip():
            k = runtime_key.strip()
            return len(k) >= 10 and "your_tavily_api_key" not in k.lower()
        return self.is_tavily_connected

    @property
    def gemini_status(self) -> str:
        """Safe status string for UI: 'Connected' or 'Not Configured'."""
        return "Connected" if self.is_gemini_connected else "Not Configured"

    @property
    def tavily_status(self) -> str:
        """Safe status string for UI: 'Connected' or 'Not Configured'."""
        return "Connected" if self.is_tavily_connected else "Not Configured"

    # Predefined verdict classifications for the multi-agent pipeline
    VERDICTS = (
        "VERIFIED TRUE",
        "MOSTLY TRUE",
        "MIXED / HALF TRUE",
        "MOSTLY FALSE",
        "DEBUNKED / FALSE",
        "UNVERIFIED / INSUFFICIENT EVIDENCE",
    )

    def reload(self):
        """Forces reloading from .env for live configuration updates."""
        load_dotenv(override=True)

    def __repr__(self) -> str:
        """Ensures that printing settings never leaks keys in logs or exceptions."""
        return (
            f"<Settings model='{self.gemini_model}' "
            f"gemini_status='{self.gemini_status}' "
            f"search_engine='{self.search_engine}' "
            f"tavily_status='{self.tavily_status}'>"
        )

    def __str__(self) -> str:
        return self.__repr__()


# Centralized singleton instance
settings = Settings()
