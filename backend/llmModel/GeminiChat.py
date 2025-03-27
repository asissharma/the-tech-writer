import google.generativeai as genai
from typing import Optional, List
from pydantic import BaseModel

# -------------------------------
# Define the Request Model
# -------------------------------
class GenerateRequest(BaseModel):
    prompt: str
    history: Optional[List[str]] = []
    system_instruction: Optional[str] = None

# -------------------------------
# Gemini (Google Generative AI) Setup
# -------------------------------

# Configure Google Generative AI with your API key.
genai.configure(api_key="AIzaSyDzbsl78nTvQQ2BRBo65rRclKZ9ttSc63s")  # Replace with your actual API key

# Generation configuration for Gemini.
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Default system instruction
DEFAULT_SYSTEM_INSTRUCTION = (
    "You are a helpful assistant. Please provide detailed and accurate responses."
)

def generate_text_gemini(request: GenerateRequest) -> dict:
    """
    Generates text using Google Generative AI (Gemini).
    """
    try:
        # Use the provided system instruction or default to the predefined one.
        system_instruction = request.system_instruction or DEFAULT_SYSTEM_INSTRUCTION

        # Initialize the Gemini model with the system instruction.
        gemini_model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction=system_instruction,
        )

        # Start a chat session with optional history.
        chat_session = gemini_model.start_chat(history=request.history or [])

        # Send the prompt to the Gemini model.
        response = chat_session.send_message(request.prompt)

        # Return the generated text.
        return {"response": response.text}
    except Exception as e:
        raise Exception(f"Gemini generation error: {e}")
