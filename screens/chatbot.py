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

    vector_store_dirs = get_vector_store_dirs()
    if not vector_store_dirs:
        st.info("No transcripts processed yet. Go to 'Summary & Process' to start.")
        return

    display_names = [name.replace(".faiss", "") for name in vector_store_dirs]
    selected_display_name = st.selectbox("Choose a vector db:", display_names)

    if selected_display_name:
        selected_vs_name = f"{selected_display_name}.faiss"
        vector_store_path = os.path.join(Config.Folders.VECTOR_STORE_DIR, selected_vs_name)

        @st.cache_resource
        def get_rag_chain(_vs_path):
            try:
                embeddings = get_embedding_001()
                vector_store = get_vector_store()
                retriever = vector_store.as_retriever()
                template = Config.Prompts.CHATBOT_PROMPT
                prompt = ChatPromptTemplate.from_template(template)
                
                return ({"context": retriever, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser())
            except Exception as e:
                st.error(f"Failed to load vector store or build RAG chain: {e}")
                return None

        rag_chain = get_rag_chain(vector_store_path)
        if not rag_chain: st.stop()
        
        if "messages" not in st.session_state or st.session_state.get("current_vs") != selected_vs_name:
            st.session_state.messages = []
            st.session_state.current_vs = selected_vs_name

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