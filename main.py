import chromadb
import google.generativeai as genai
from api import value
import json
import os
from vector_store import retrieve_context
from pdf_processing import update_knowledge_base

# Configure the generative model and functions
genai.configure(api_key=value)

generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
)


def takeCommand():
    try:
        query = input("User: ")
        return query
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Some Error Occurred. Sorry from Luna"


def chat(query):
    context = retrieve_context(query)

    if context:
        full_query = f"Context: {context}\nQuery: {query}"
    else:
        full_query = f"Query: {query}. I don't have specific context for this query."

    for _ in range(3):  # Retry up to 3 times
        try:
            response = model.generate_content([full_query])

            # Debugging: Print the type and content of the response
            # print(f"Response Type: {type(response)}")
            # print(f"Response Content: {response}")

            # Assuming response is an object with a 'text' attribute
            if hasattr(response, 'text'):
                response_text = response.text
            else:
                response_text = "Sorry, I'm unable to assist at the moment."

        except Exception as e:
            print(f"Error occurred: {e}. Retrying...")
            response_text = "Sorry, I'm unable to assist at the moment."

    # Fallback mechanism for off-topic or irrelevant queries
    if not context and "Sorry" in response_text:
        fallback_query = f"General response for: {query}"
        try:
            fallback_response = model.generate_content([fallback_query])
            if hasattr(fallback_response, 'text'):
                return fallback_response.text
            else:
                return "I'm not sure how to respond to that. Can you please provide more details or ask a different question?"
        except Exception as e:
            print(f"Fallback error occurred: {e}.")
            return "I'm not sure how to respond to that. Can you please provide more details or ask a different question?"

    return response_text


def save_conversation(conversation, file_path='conversations.json'):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                conversations = json.load(f)
        else:
            conversations = []

        conversations.append(conversation)

        with open(file_path, 'w') as f:
            json.dump(conversations, f, indent=4)

        # Save conversation to ChromaDB
        collection = chromadb.Client().get_or_create_collection(name="conversation_context")
        collection.add(
            documents=[conversation['User'] + ": " + conversation['Luna']],
            ids=[str(len(conversations))],
            metadatas=[{"conversation_id": str(len(conversations))}]
        )
    except Exception as e:
        print(f"Failed to save conversation: {e}")


conversations = []
# Load previous conversations from the JSON file
if os.path.exists('conversations.json'):
    with open('conversations.json', 'r') as f:
        conversations = json.load(f)

if __name__ == '__main__':
    # Update the knowledge base with new PDFs
    pdf_directory = 'pdf_content'
    update_knowledge_base(pdf_directory)

    while True:
        query = takeCommand()
        if query.lower() in ["exit", "quit"]:
            break
        response = chat(query)
        print("Luna:", response)

        # Save the conversation
        conversation = {"User": query, "Luna": response}
        save_conversation(conversation)