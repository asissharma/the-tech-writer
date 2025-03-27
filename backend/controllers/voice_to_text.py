import io
import speech_recognition as sr
from pydub import AudioSegment

def convert_voice_to_text(audio_data: bytes, file_format: str) -> dict:
    """
    Converts provided audio data (in bytes) to text.
    Supports conversion from various formats (e.g., mp3, flac, aiff) to WAV.
    
    Args:
        audio_data (bytes): The audio file data.
        file_format (str): Format of the input audio (e.g., "mp3", "flac", "aiff", "wav").
        
    Returns:
        dict: A dictionary containing the recognized text.
    """
    recognizer = sr.Recognizer()
    
    # If the input is already in WAV format, use it directly.
    if file_format.lower() == "wav":
        audio_file = io.BytesIO(audio_data)
    else:
        # Convert the audio data to WAV using pydub with explicit parameters.
        try:
            # Load the audio data from the provided file format
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format=file_format)
        except Exception as e:
            return {"converted_text": f"Error reading audio file: {e}"}
        
        # Export the audio segment to a BytesIO stream in WAV format.
        # We set parameters to force a mono channel and a standard sample rate.
        wav_io = io.BytesIO()
        try:
            audio_segment.export(wav_io, format="wav", parameters=["-ac", "1", "-ar", "16000"])
        except Exception as e:
            return {"converted_text": f"Error converting audio to WAV: {e}"}
        wav_io.seek(0)
        audio_file = wav_io

    try:
        # Use SpeechRecognition to process the WAV audio
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        recognized_text = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        recognized_text = "Speech recognition could not understand the audio."
    except sr.RequestError as e:
        recognized_text = f"Error with the speech recognition service: {e}"
    except Exception as e:
        recognized_text = f"Unexpected error: {e}"
    
    return {"converted_text": recognized_text}
