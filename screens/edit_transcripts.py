from utils.config import Config
import streamlit as st
import os
from utils.get_folder_contents import get_transcript_files
from function.vector_db_ops import update_vector_store
def edit_transcript():
    st.header("Edit and Refine Transcripts")
    
    transcript_files = get_transcript_files()
    
    if not transcript_files:
        st.info("No transcripts found. Process a media file first.")
    else:
        selected_transcript = st.selectbox("Choose a transcript to edit:", transcript_files, key="transcript_edit_select")
        
        if selected_transcript:
            transcript_path = os.path.join(Config.Folders.TRANSCRIPT_DIR, selected_transcript)
            with open(transcript_path, "r", encoding="utf-8") as f:
                original_text = f.read()
            
            edited_text = st.text_area("Edit the transcript:", value=original_text, height=400, key=f"editor_{selected_transcript}")
            
            if st.button("Save Changes"):
                with open(transcript_path, "w", encoding="utf-8") as f:
                    f.write(edited_text)
                st.success(f"Transcript '{selected_transcript}' saved!")
                update_vector_store()
                st.success("Vector store updated with edited transcripts.")
                
if __name__ == "__main__":
    edit_transcript()