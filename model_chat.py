import requests
import json
import sys
import os
from dotenv import load_dotenv

load_dotenv()
URL = os.getenv("OLLAMA_URL")
MODEL = os.getenv("OLLAMA_MODEL")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT_SFW_EN")

def chat_with_ollama():
    try:
        response = requests.get(f"{URL}/tags")
        available_models = [model["name"] for model in response.json()["models"]]
        if MODEL not in available_models:
            print(f"Model '{MODEL}' not found locally. Pulling from Ollama...")
            pull_response = requests.post(f"{URL}/pull", json={"name": MODEL})
            if pull_response.status_code != 200:
                print(f"Error pulling model: {pull_response.text}")
                return
            print(f"Model '{MODEL}' successfully pulled.")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Ollama. Make sure Ollama is running.")
        return
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print(f"\n--- Chat with {MODEL} ---")
    print("Type 'exit' or 'quit' to end the conversation.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Ending chat session.")
            break
        messages.append({"role": "user", "content": user_input})
        payload = {
            "model": MODEL,
            "messages": messages,
            "stream": True
        }
        print("\nAI: ", end="", flush=True)
        assistant_response = ""
        try:
            with requests.post(f"{URL}/chat", json=payload, stream=True) as response:
                for line in response.iter_lines():
                    if line:
                        json_line = json.loads(line)
                        if 'message' in json_line:
                            message_content = json_line['message'].get('content', '')
                            if message_content:
                                print(message_content, end="", flush=True)
                                assistant_response += message_content
                        if json_line.get('done', False):
                            print("\n")
                            break
        except requests.exceptions.RequestException as e:
            print(f"\nError: {e}")
            continue
        messages.append({"role": "assistant", "content": assistant_response})

if __name__ == "__main__":
    try:
        requests.get(URL)
        chat_with_ollama()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Ollama. Please make sure Ollama is running.")
        print("You can start Ollama by running the 'ollama serve' command.")
        sys.exit(1)