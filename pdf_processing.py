from PyPDF2 import PdfReader
import os
import chromadb
import uuid

# Initialize ChromaDB client and collection
client = chromadb.Client()
collection_name = "knowledge_base"
collection = client.get_or_create_collection(name=collection_name)

def process_pdf(file_path):
    """Extract text from a PDF file and add it to the ChromaDB vector store."""
    try:
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

        # Generate a unique ID for the document
        doc_id = str(uuid.uuid4())

        # Add extracted text to ChromaDB
        collection.add(documents=[text], ids=[doc_id])
        print(f"Processed and added {file_path} to the knowledge base with ID {doc_id}.")
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

def update_knowledge_base(directory):
    """Process all PDF files in the given directory and update the ChromaDB vector store."""
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            process_pdf(file_path)
