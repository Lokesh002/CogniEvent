import streamlit as st
import os
from utils.config import Config

def main():
    os.makedirs(Config.Folders.VIDEO_DIR, exist_ok=True)
    os.makedirs(Config.Folders.AUDIO_DIR, exist_ok=True)
    os.makedirs(Config.Folders.TRANSCRIPT_DIR, exist_ok=True)
    os.makedirs(Config.Folders.VECTOR_STORE_DIR, exist_ok=True)
    
    pg=st.navigation([st.Page("screens/homepage.py",title="Home"),st.Page("screens/upload_data.py", title="Upload Data")])
    pg.run()

if __name__ == "__main__":
    main()