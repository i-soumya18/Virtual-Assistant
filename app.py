# Filename: streamlit_ui.py
import streamlit as st
import os
from main import chat, save_conversation
from pdf_processing import update_knowledge_base

# Set the PDF content directory
PDF_CONTENT_DIR = "pdf_content"

# Function to handle PDF upload
def handle_pdf_upload(uploaded_file):
    if uploaded_file is not None:
        file_path = os.path.join(PDF_CONTENT_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File {uploaded_file.name} uploaded successfully!")
        update_knowledge_base(PDF_CONTENT_DIR)  # Update the knowledge base with the new PDF
    else:
        st.warning("No file uploaded. Using existing PDFs.")

# Streamlit UI
def main():
    st.title("AI-Powered Chatbot with PDF Knowledge Base")

    # PDF Upload Section
    st.header("Upload a PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    handle_pdf_upload(uploaded_file)

    # Chat Section
    st.header("Chat with the Bot")
    query = st.text_input("You:", placeholder="Type your question here...")
    if st.button("Send"):
        if query:
            response = chat(query)
            st.text_area("Luna:", value=response, height=200)

            # Optionally save the conversation
            conversation = {"User": query, "Luna": response}
            save_conversation(conversation)

# Run the app
if __name__ == "__main__":
    if not os.path.exists(PDF_CONTENT_DIR):
        os.makedirs(PDF_CONTENT_DIR)
    main()
