import chromadb

# Initialize ChromaDB client and collection
client = chromadb.Client()
collection_name = "knowledge_base"
collection = client.get_or_create_collection(name=collection_name)

def retrieve_context(query):
    """Retrieve context from ChromaDB based on the query."""
    results = collection.query(query_texts=[query], n_results=3)

    # Flatten the list of lists to a single list of strings
    documents = [doc for sublist in results['documents'] for doc in sublist]

    if documents:
        context = " ".join(documents)
        return context
    return ""
