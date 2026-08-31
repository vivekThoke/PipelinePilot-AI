from google import genai
from google.genai import types

from app.core.config import get_settings
from app.schemas.agent import LeadAnalysis

class GeminiService:
    """Service responsible for Gemini AI interactions."""
    
    def __init__(self) -> None:
        settings = get_settings()
        
        self.model = settings.gemini_api_model
        
        self.client = genai.Client(
            api_key=settings.gemini_api_key,
        ) 
        
    
    def analyze_lead(
        self,
        lead: dict[str, object]
    ) -> LeadAnalysis:
        """Analyze a CRM lead and recommend the next action."""
        
        prompt = f"""
            You are a Revenue Operations AI assistant.

            Your job is to analyze CRM lead information and recommend
            the next action.

            Important rules:

            - Base your reasoning only on the provided CRM data.
            - Do not invent information.
            - Do not assume a meeting happened if it is not in the notes.
            - Do not claim that the lead expressed interest unless
            the CRM data supports it.
            - Prefer "no_action" when there is insufficient evidence.
            - A high-value lead does not automatically mean the lead
            should be qualified.
            - Your output must follow the requested schema.

            CRM Lead:

            {lead}
            """
            
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=LeadAnalysis
            )
        )
        
        return LeadAnalysis.model_validate_json(
            response.text
        )