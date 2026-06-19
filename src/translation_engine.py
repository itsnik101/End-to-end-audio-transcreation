import logging
from google import genai
from google.genai import types
from google.genai.errors import APIError
from pydantic import BaseModel, Field, ValidationError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from config import GEMINI_API_KEY, DEFAULT_MODEL, TRANSCREATION_TEMPERATURE

logger = logging.getLogger("audix.translation")

class DialogueLine(BaseModel):
    character_name: str = Field(description="Name of the character speaking")
    translated_dialogue: str = Field(description="Localized dialogue adapting idioms natively")
    emotional_tone: str = Field(description="Expressive tone marker")

class LocalizedScript(BaseModel):
    original_title: str = Field(description="The matching title of the incoming source text")
    target_language: str
    story_hook_summary: str = Field(description="A highly engaging 2-sentence marketing summary for trailers.")
    dialogue_flow: list[DialogueLine]

class TranslationEngine:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    @retry(
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(APIError),
        reraise=True
    )
    def transcreate_script(self, raw_script: str, target_lang: str, title: str) -> LocalizedScript:
        system_instruction = (
            "You are an expert audio show producer and screenwriter for AudiX Engine. "
            "Adapt raw scripts into regional variations. Change jokes and cultural references to look native."
        )

        prompt = f"Title: {title}\nAnalyze this raw script and transcreate it into {target_lang}:\n\n\"\"\"{raw_script}\"\"\""
        logger.info(f"Dispatching transcreation request to Gemini for show: '{title}'")
        
        response = self.client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=LocalizedScript,
                temperature=TRANSCREATION_TEMPERATURE
            )
        )
        
        raw_text = response.text
        try:
            return LocalizedScript.model_validate_json(raw_text)
        except ValidationError as ve:
            logger.error(f"Pydantic schema validation failure. Raw response: {raw_text}")
            raise ValueError("Upstream AI model failed content structure validation.") from ve