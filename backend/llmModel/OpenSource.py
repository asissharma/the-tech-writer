# import os
# from llama_cpp import Llama
# from typing import Optional,List
# from pydantic import BaseModel

# # -------------------------------
# # Open Source LLM Setup (llama-cpp-python)
# # -------------------------------
# class GenerateRequest(BaseModel):
#     prompt: str
#     history: Optional[List[str]] = []
#     system_instruction: Optional[str] = None
# # Construct the absolute path to the gguf model file.
# current_dir = os.path.dirname(os.path.abspath(__file__))
# model_path = os.path.join(current_dir, '..', 'llmModels', 'Llama-3.2-1B-Instruct-Uncensored.f16.gguf')

# # Allow overriding the model path via an environment variable.
# MODEL_PATH = os.getenv("LLM_MODEL_PATH", model_path)

# # Initialize the open source LLM.
# try:
#     open_source_llm = Llama(model_path=MODEL_PATH, n_ctx=512)
# except Exception as e:
#     open_source_llm = None
#     print(f"Error loading open source LLM model from {MODEL_PATH}: {e}")

# def generate_text_open_source(request: GenerateRequest) -> dict:
#     """
#     Generates text using the open source LLM via llama-cpp-python.
#     """
#     if open_source_llm is None:
#         return {"response": "Error: Open source LLM model not loaded."}
    
#     # Construct a prompt for the open source model.
#     prompt = (
#         "You are a creative writing assistant. Based on the following prompt, generate an engaging response.\n\n"
#         f"Prompt: {request.prompt}\n\nResponse:"
#     )
    
#     try:
#         # Generate text with controlled parameters.
#         response = open_source_llm(
#             prompt=prompt,
#             max_tokens=150,
#             temperature=0.9,
#             top_p=0.95,
#             echo=False
#         )
#         generated_text = response["choices"][0]["text"].strip()
#     except Exception as e:
#         generated_text = f"Error generating text with open source model: {e}"
    
#     return {"response": generated_text}

def generate_text_open_source()-> dict:
    return true