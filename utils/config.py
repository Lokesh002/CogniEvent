class Config:
    class Folders:
        VIDEO_DIR = "Video"
        AUDIO_DIR = "Audio"
        TRANSCRIPT_DIR = "Transcripts"
        VECTOR_STORE_DIR = "Vector_Dbs"
    class Prompts:
        TRANSCRIPTION_PROMPT = """You are a highly skilled AI trained in speech recognition.
Transcribe the provided audio, identifying different speakers (write Speaker 1/2/3.. if speaker is not identified) and including timestamps like [HH:MM:SS]."""
        SUMMARIZER_PROMPT="""You are an expert at summarizing meeting transcripts. Based on this transcript, provide a 'Title', a list of 'Participants', and a bulleted list of 'Key Points'.\n\nTranscript:\n{transcript}"""
        CHATBOT_PROMPT="Answer the question based only on the following context:\n\n{context}\n\nQuestion: {question}"