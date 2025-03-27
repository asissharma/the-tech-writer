import language_tool_python
import textstat

def analyze_text(text: str) -> dict:
    """
    Analyzes the given text for spelling, grammar, and readability.
    
    Uses:
      - language_tool_python with the Public API for grammar and spell checks.
      - textstat for calculating a readability score.
      
    Args:
        text (str): The input text to analyze.
        
    Returns:
        dict: A dictionary containing the original text, detected spelling errors,
              grammar suggestions, and a readability score.
    """
    # Always create a new instance to ensure a fresh connection
    tool = language_tool_python.LanguageToolPublicAPI('en-US')
    try:
        matches = tool.check(text)
    except Exception as e:
        # If an error occurs, reinitialize and try again
        tool = language_tool_python.LanguageToolPublicAPI('en-US')
        matches = tool.check(text)
    
    # Optionally, if the tool exposes its underlying session, close it to free resources.
    if hasattr(tool, "_session"):
        tool._session.close()
    
    # Process the matches into spelling errors and grammar suggestions
    spelling_errors = []
    grammar_suggestions = []
    for match in matches:
        msg = match.message.lower()
        if "spelling" in msg:
            spelling_errors.append(match.message)
        else:
            grammar_suggestions.append(match.message)
    
    # Calculate the readability score using textstat
    readability_score = textstat.flesch_reading_ease(text)
    
    return {
        "text": text,
        "spelling_errors": spelling_errors,
        "grammar_suggestions": grammar_suggestions,
        "readability_score": readability_score
    }
