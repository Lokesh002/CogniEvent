import streamlit as st
import os
import shutil
from utils.config import Config
from utils.get_folder_contents import get_video_files, get_audio_files, get_base_filename, get_transcript_files, get_vector_store_dirs
def file_manager():
    st.header("File Management")

    def delete_associated_files(base_name):
        """Deletes all files associated with a base filename."""
        # Note: Audio file could be mp3, wav, or m4a, but extracted audio is always mp3
        audio_extensions = ['.mp3', '.wav', '.m4a']
        for ext in audio_extensions:
            audio_path = os.path.join(Config.Folders.AUDIO_DIR, f"{base_name}{ext}")
            if os.path.exists(audio_path): os.remove(audio_path)
        
        transcript_path = os.path.join(Config.Folders.TRANSCRIPT_DIR, f"{base_name}_transcript.txt")
        if os.path.exists(transcript_path): os.remove(transcript_path)
        
        vector_store_path = os.path.join(Config.Folders.VECTOR_STORE_DIR, f"{base_name}.faiss")
        if os.path.exists(vector_store_path): shutil.rmtree(vector_store_path)

    # --- Video Files Section ---
    st.subheader("Uploaded Video Files")
    video_files = get_video_files()
    if not video_files: st.info("No video files have been uploaded yet.")
    else:
        for filename in video_files:
            col1, col2, col3 = st.columns([4, 1, 1])
            with col1: st.text(filename)
            with col2:
                with open(os.path.join(Config.Folders.VIDEO_DIR, filename), "rb") as f:
                    st.download_button("⬇️", f, file_name=filename, mime="video/mp4", key=f"dl_vid_{filename}", help=f"Download {filename}")
            with col3:
                if st.button("🗑️", key=f"del_vid_{filename}", help=f"Delete video and all associated files"):
                    base_name = get_base_filename(filename)
                    os.remove(os.path.join(Config.Folders.VIDEO_DIR, filename)) # Delete video
                    delete_associated_files(base_name) # Delete everything else
                    st.success(f"Deleted '{filename}' and all its associated files.")
                    st.rerun()

    st.markdown("---")

    # --- Audio Files Section ---
    st.subheader("Uploaded & Extracted Audio Files")
    audio_files = get_audio_files()
    if not audio_files: st.info("No audio files available.")
    else:
        for filename in audio_files:
            col1, col2, col3 = st.columns([4, 1, 1])
            with col1: st.text(filename)
            with col2:
                with open(os.path.join(Config.Folders.AUDIO_DIR, filename), "rb") as f:
                    st.download_button("⬇️", f, file_name=filename, mime="audio/mpeg", key=f"dl_aud_{filename}", help=f"Download {filename}")
            with col3:
                if st.button("🗑️", key=f"del_aud_{filename}", help=f"Delete audio and associated files (transcript, vector store)"):
                    base_name = get_base_filename(filename)
                    delete_associated_files(base_name)
                    st.success(f"Deleted '{filename}' and its associated files.")
                    st.rerun()

    st.markdown("---")
    st.subheader("Generated Transcript Files")
    transcript_files = get_transcript_files()
    if not transcript_files:
        st.info("No transcripts have been generated yet.")
    else:
        for filename in transcript_files:
            file_path = os.path.join(Config.Folders.TRANSCRIPT_DIR, filename)
            col1, col2, col3 = st.columns([4, 1, 1])

            with col1:
                st.text(filename)
            with col2:
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="⬇️", data=f, file_name=filename, mime="text/plain",
                        key=f"download_txt_{filename}", help=f"Download {filename}"
                    )
            with col3:
                if st.button("🗑️", key=f"delete_txt_{filename}", help=f"Delete {filename} and its vector store"):
                    base_name = filename.replace("_transcript.txt", "")
                    # Delete transcript
                    os.remove(file_path)
                    # Delete associated vector store
                    vector_store_path = os.path.join(Config.Folders.VECTOR_STORE_DIR, f"{base_name}.faiss")
                    if os.path.exists(vector_store_path):
                        shutil.rmtree(vector_store_path)
                    
                    st.success(f"Deleted '{filename}' and its associated vector store.")
                    st.rerun()
    
    st.markdown("---")

    # --- Vector Store Section ---
    st.subheader("Generated Vector Stores")
    vector_store_dirs = get_vector_store_dirs()
    if not vector_store_dirs:
        st.info("No vector stores have been created yet.")
    else:
        for dirname in vector_store_dirs:
            dir_path = os.path.join(Config.Folders.VECTOR_STORE_DIR, dirname)
            col1, col2 = st.columns([4, 1])
            with col1:
                st.text(dirname)
            with col2:
                if st.button("🗑️", key=f"delete_vs_{dirname}", help=f"Delete vector store '{dirname}'"):
                    shutil.rmtree(dir_path)
                    st.success(f"Deleted vector store '{dirname}'.")
                    st.rerun()

if __name__ == "__main__":
    file_manager()
