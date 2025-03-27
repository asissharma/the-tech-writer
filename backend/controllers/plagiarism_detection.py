# controllers/plagiarism_detection.py
from llmModel.GeminiChat import generate_text_gemini  # Assuming this is your Gemini function
from pydantic import BaseModel
from typing import Optional,List

class GenerateRequest(BaseModel):
    prompt: str
    history: Optional[List[str]] = []
    system_instruction: Optional[str] = None

def check_plagiarism(request: GenerateRequest) -> dict:
    """
    Checks the provided text for potential plagiarism using Gemini.
    Constructs a prompt to instruct Gemini to analyze the text for plagiarism,
    then returns Gemini's response.

    Args:
        request (GenerateRequest): The request object containing the prompt, history, etc.
    
    Returns:
        dict: The plagiarism analysis result.
    """
    # Construct a new prompt for plagiarism detection based on the provided prompt
    modified_prompt = (
        "You are a plagiarism detection assistant. Analyze the following text for potential plagiarism "
        "by comparing it with known sources. Provide details on any similarity detected.\n\n"
        f"Text: {request.prompt}\n\nAnalysis:"
    )
    
    # Create a new request object with the modified prompt
    new_request = GenerateRequest(
        prompt=modified_prompt,
        history=request.history,
        system_instruction=request.system_instruction
    )
    
    try:
        response = generate_text_gemini(new_request)
        return {"plagiarism_check": response.get("response", "No response from Gemini.")}
    except Exception as e:
        return {"plagiarism_check": f"Error during plagiarism check: {e}"}
