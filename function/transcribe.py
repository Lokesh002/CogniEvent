from models.llms.google_llm import gemini_2_5_flash as llm
import os
import base64
from langchain_core.messages import HumanMessage
from utils.config import Config
def transcribe_audio_with_gemini(audio_file_path):
    """Transcribes an audio file using the Gemini model."""
    with open(audio_file_path, "rb") as audio_file:
        audio_data = base64.b64encode(audio_file.read()).decode("utf-8")
    
    mime_type = "audio/mpeg" if audio_file_path.endswith('.mp3') else f"audio/{os.path.splitext(audio_file_path)[1][1:]}"

    prompt_text = Config.Prompts.TRANSCRIPTION_PROMPT
    message = HumanMessage(content=[{"type": "text", "text": prompt_text}, 
                                    {"type": "audio", "source_type": "base64", "data": audio_data, "mime_type": mime_type}])

    try:
        response = llm.invoke([message])
        transcript = response.content
        return transcript
    except Exception as e:
        raise RuntimeError(f"An error occurred during transcription: {e}")
        