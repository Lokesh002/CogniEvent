import streamlit as st
import requests

def homepage():
    st.set_page_config(page_title="CogniEvent - Home", page_icon="🏠", layout="wide")    
    st.title("Welcome to the CogniEvent App 🎉")
    st.subheader("Your Personal Assistant for Meeting Transcription and Summarization")

if __name__ == "__main__":
    homepage()
