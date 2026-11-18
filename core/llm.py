"""
TruthLens AI - LLM Client (Google Gemini API Wrapper)
=====================================================
Encapsulates communication with Google's Gemini models using the official SDK.
Features prioritized model selection (gemini-3.1-flash-lite), automatic fallbacks,
structured JSON extraction, and strict credential protection.
"""

import json
import re
import logging
from typing import Optional, Any, Dict, List
from config import settings

logger = logging.getLogger(__name__)


class GeminiClient:
    """Wrapper client managing Gemini API requests and structured responses."""

    CANDIDATE_MODELS = [
        "gemini-3.1-flash-lite",
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
        "gemini-3.8-flash",
    ]

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or settings.gemini_api_key
        # Default directly to gemini-3.1-flash-lite if model_name is 2.5-flash or empty
        preferred = model_name or settings.gemini_model
        if not preferred or "2.5-flash" in preferred:
            preferred = "gemini-3.1-flash-lite"
        self.model_name = preferred
        self._client = None
        self._active_model: str = self.model_name
        self._initialize_client()

    def _initialize_client(self):
        """Initializes the modern Google GenAI client safely."""
        if not self.api_key or "your_gemini_api_key" in self.api_key.lower():
            logger.warning("Gemini API key is not configured. LLM calls will fail until configured.")
            return

        try:
            from google import genai
            self._client = genai.Client(api_key=self.api_key)
            logger.info(f"Initialized Google GenAI client with model: {self._active_model}")
        except Exception as e:
            logger.error(f"Failed to initialize Google GenAI SDK: {type(e).__name__}")

    def generate_text(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """
        Sends a prompt to Gemini with automatic model fallback and returns the textual response.
        """
        if not self._client:
            raise ValueError("Gemini client is not initialized. Please verify GEMINI_API_KEY in .env or st.secrets.")

        models_to_try = [self._active_model]
        for m in self.CANDIDATE_MODELS:
            if m not in models_to_try:
                models_to_try.append(m)

        last_error = None
        for model_id in models_to_try:
            try:
                full_contents = prompt
                if system_instruction:
                    full_contents = f"System Instruction:\n{system_instruction}\n\nTask:\n{prompt}"

                resp = self._client.models.generate_content(
                    model=model_id,
                    contents=full_contents,
                )
                self._active_model = model_id
                return resp.text.strip() if resp.text else ""
            except Exception as e:
                err_msg = str(e)
                if "404" in err_msg or "NOT_FOUND" in err_msg:
                    logger.warning(f"Model {model_id} not available, trying fallback...")
                    last_error = e
                    continue
                else:
                    logger.error(f"Gemini generation error on {model_id}: {type(e).__name__}")
                    raise RuntimeError(f"Gemini API error: {type(e).__name__}") from None

        raise RuntimeError(f"All candidate Gemini models failed. Last error: {last_error}")

    def generate_json(self, prompt: str, system_instruction: Optional[str] = None) -> Any:
        """
        Sends a prompt expecting structured JSON and parses the response safely.
        Strips markdown code fences (```json ... ```) automatically.
        """
        json_instruction = (
            "You are a rigorous structured fact-checking AI. "
            "You must output ONLY valid, parseable JSON without any conversational text or markdown formatting."
        )
        if system_instruction:
            combined_instruction = f"{system_instruction}\n\n{json_instruction}"
        else:
            combined_instruction = json_instruction

        raw_text = self.generate_text(prompt, system_instruction=combined_instruction)

        # Clean markdown code blocks
        clean_text = raw_text.strip()
        if clean_text.startswith("```"):
            clean_text = re.sub(r"^```(?:json)?\s*", "", clean_text)
            clean_text = re.sub(r"\s*```$", "", clean_text)
            clean_text = clean_text.strip()

        # Find first JSON object or array
        match = re.search(r"(\{.*\}|\[.*\])", clean_text, re.DOTALL)
        if match:
            clean_text = match.group(1)

        try:
            return json.loads(clean_text)
        except json.JSONDecodeError as err:
            logger.error(f"JSON parsing error: {err}. Raw text was: {raw_text[:200]}")
            raise ValueError(f"Failed to parse structured JSON from Gemini response: {err}")
