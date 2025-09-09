import streamlit as st
from utils.video_to_audio import video_buffer_to_audio
def upload_data():
    st.header("Upload Data")
    uploaded_file = st.file_uploader("Choose a file", type=["mp4", "mov", "avi", "mp3", "wav", "m4a"])
    if uploaded_file is not None:
        file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type, "filesize": f"{round(uploaded_file.size/1024/1024,2)} MB"}
        st.write(file_details)
        if st.button("Upload"):
            # save file in a folder "Audio" or Video based on file type
            if uploaded_file.type in ["audio/mpeg", "audio/wav", "audio/m4a", "audio/mp4"]:
                with open(f"Audio/{uploaded_file.name}", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success("File Uploaded")
                
            elif uploaded_file.type in ["video/mp4", "video/mov","video/avi"]:
                video_buffer_to_audio(uploaded_file.getbuffer(), f"Audio/{uploaded_file.name.split('.')[0]}.mp3")
                st.success("File Uploaded and saved as audio file")

           
if __name__ == "__main__":
    upload_data()