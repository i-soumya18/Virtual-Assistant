# chat_cli.py
import requests

def chat_with_bot(user_input):
    response = requests.post("http://localhost:8000/chat", json={"user_input": user_input})
    print("Bot:", response.json()['response'])

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        chat_with_bot(user_input)
