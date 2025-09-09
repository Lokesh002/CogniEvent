import streamlit as st
from utils.get_folder_contents import get_audio_files, get_base_filename
from utils.config import Config
import os
from function.transcribe import transcribe_audio_with_gemini
from function.summarize import summarize_transcript
from function.vector_db_ops import create_and_save_vector_store

def process_and_summarize():

    st.title("Meeting Transcription and Summarization 🎙️")
    st.markdown("---")

    st.write("Select an Audio File to Process")
    
    audio_files = get_audio_files()
    
    if not audio_files:
        st.info("No audio files found. Please upload a media file first.")
    else:
        selected_audio = st.selectbox("Choose an audio file:", audio_files, key="audio_select")
        
        if st.button("Process and Summarize Audio"):
            audio_path = os.path.join(Config.Folders.AUDIO_DIR, selected_audio)
            base_filename = get_base_filename(selected_audio)
            transcript_filename = f"{base_filename}_transcript.txt"
            transcript_path = os.path.join(Config.Folders.TRANSCRIPT_DIR, transcript_filename)
            
            transcript_text = ""
            
            if os.path.exists(transcript_path):
                st.info("Loading existing transcript.")
                with open(transcript_path, "r", encoding="utf-8") as f:
                    transcript_text = f.read()
            else:
                with st.spinner("Transcribing audio... This may take a while for long files."):
                    transcript_text = transcribe_audio_with_gemini( audio_path)
                
                if transcript_text:
                    with open(transcript_path, "w", encoding="utf-8") as f:
                        f.write(transcript_text)
            
            if not transcript_text:
                 st.error("Failed to generate or load a transcript.")
            else:
                with st.expander("View Full Transcript"):
                    st.text_area("Transcript", transcript_text, height=300)
                
                try:
                    create_and_save_vector_store(transcript_text, "faiss_vdb")
                except RuntimeError as e:
                    st.error(str(e))
                
                st.markdown("---")
                
                st.subheader("Meeting Summary")
                with st.spinner("Generating summary..."):
                    try:
                        summary = summarize_transcript( transcript_text)
                        st.markdown(summary)
                    except Exception as e:
                        st.error(f"Error generating summary: {e}")
if __name__ == "__main__":
    process_and_summarize()
