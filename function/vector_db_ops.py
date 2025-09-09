from langchain_text_splitters import RecursiveCharacterTextSplitter
from models.llms.google_llm import gemini_2_5_flash as llm
from models.embedding_models.google_EM import get_embedding_001
from langchain_community.vectorstores import FAISS
import os
import shutil
from utils.config import Config
import streamlit as st

def create_and_save_vector_store(transcript, base_filename):
    """Chunks transcript and saves it as a FAISS vector store."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=200)
    embedding=get_embedding_001()
    chunks = text_splitter.split_text(text=transcript)
    try:
        if not os.path.exists(f"{Config.Folders.VECTOR_STORE_DIR}/faiss_vdb.faiss"):
            vector_store = FAISS.from_texts(chunks, embeddings=embedding)
        else:
            vector_store = FAISS.load_local(f"{Config.Folders.VECTOR_STORE_DIR}/faiss_vdb.faiss", embeddings=embedding, allow_dangerous_deserialization=True)
            vector_store.add_texts(chunks)
        
        vector_store_path = os.path.join(Config.Folders.VECTOR_STORE_DIR, f"faiss_vdb.faiss")       
        vector_store.save_local(vector_store_path)
    except Exception as e:
        raise RuntimeError(f"An error occured while creating vecotr db: {e}")
    
def get_vector_store():
    """Loads a FAISS vector store by name."""
    vector_store_path = os.path.join(Config.Folders.VECTOR_STORE_DIR, f"faiss_vdb.faiss")
    if not os.path.exists(vector_store_path):
        raise FileNotFoundError(f"Vector store 'faiss_vdb' not found.")
    try:
        embedding=get_embedding_001()
        vector_store = FAISS.load_local(vector_store_path, embeddings=embedding, allow_dangerous_deserialization=True)
        return vector_store
    except Exception as e:
        raise RuntimeError(f"An error occurred while loading vector store: {e}")