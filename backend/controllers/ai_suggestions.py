from llmModel.GeminiChat import generate_text_gemini
from llmModel.OpenSource import generate_text_open_source

def generate_suggestion(request, source: str) -> dict:
    """
    Generate a creative suggestion based on the provided request and source.
    
    Args:
        request (GenerateRequest): The request object containing prompt and other parameters.
        source (str): The source to use ("gemini" or "open_source").
    
    Returns:
        dict: The result of the text generation.
    """
    if source.lower() == "gemini":
        # Define the additional system instruction for suggestions.
        additional_instruction = (
            "You are a suggestor. Please generate a continuous sentence that suggests the next 10 words as a seamless continuation of the given data."
        )
        # Append the additional instruction to the system_instruction in the request,
        # or set it if it is not provided.
        if request.system_instruction:
            request.system_instruction = f"{request.system_instruction} {additional_instruction}"
        else:
            request.system_instruction = additional_instruction
        
        # Call the Gemini API function with the updated request.
        suggestion_result = generate_text_gemini(request)
    else:
        # Call the open source LLM function if source is not Gemini.
        suggestion_result = generate_text_open_source(request)
    return suggestion_result
