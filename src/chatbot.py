import requests
import fitz  # PyMuPDF
from dotenv import load_dotenv
import os

config = load_dotenv()
key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text


def query_gpt4(messages):
    headers = {
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4-1106-preview",
        "messages": messages,
    }
    res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    return res.json()


conv_history = []
pdf_path = '../data/art.pdf'
pdf_text = extract_text_from_pdf(pdf_path)
conv_history.append({"role": "user", "content": pdf_text})

while True:
    user_input = input("User: ")
    conv_history.append({"role": "user", "content": user_input})

    response_json = query_gpt4(conv_history)
    ai_response = response_json['choices'][0]['message']['content']
    print("ONER.:", ai_response)

    conv_history.append({"role": "assistant", "content": ai_response})

    if user_input.lower() in ["quit", "exit", "stop"]:
        break
