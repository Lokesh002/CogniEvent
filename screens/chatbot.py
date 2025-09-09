import os
import streamlit as st
from utils.config import Config
from utils.get_folder_contents import get_vector_store_dirs
from models.llms.google_llm import gemini_2_5_flash as llm
from function.vector_db_ops import get_vector_store
from models.embedding_models.google_EM import get_embedding_001
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser



def chatbot_page():
    st.header("Chat with Your Transcripts 💬")

    def get_rag_chain():
        try:
            # embeddings = get_embedding_001()
            vector_store = get_vector_store()
            retriever = vector_store.as_retriever()
            template = Config.Prompts.CHATBOT_PROMPT
            prompt = ChatPromptTemplate.from_template(template)
            return ({"context": retriever, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser())
        except Exception as e:
            st.error(f"Failed to load vector store or build RAG chain: {e}")
            return None

    # mtime = get_vector_db_mtime(vector_store_path)
    rag_chain = get_rag_chain()
    if not rag_chain: st.stop()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about the transcript..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = rag_chain.invoke(prompt)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    chatbot_page()