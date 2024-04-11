from django.shortcuts import render
from django.http import HttpResponse

import os
import fitz  # PyMuPDF
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings

OPENAI_API_KEY="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"

def index(request):
    return render(request, 'index.html')

# Open a pdf file and Extract text from it
def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text


@csrf_exempt
@require_http_methods(["POST"])
def chatbot_response(request):
    # Load the message from the request
    user_message = request.POST.get('message')
    conv_history = request.session.get('conv_history', [])

    if user_message.lower() in ["quit", "exit", "stop"]:
        request.session['conv_history'] = []  # Reset conversation history
        return JsonResponse({'message': "Conversation ended."})

    if 'pdf_text' not in request.session:
        # 'art.pdf' in the static files directory
        pdf_path = os.path.join(settings.BASE_DIR, 'chat', 'static', 'data', 'art.pdf')

        request.session['pdf_text'] = extract_text_from_pdf(pdf_path)

    conv_history.append({"role": "user", "content": user_message})

    ai_response = query_gpt4(conv_history)
    conv_history.append({"role": "assistant", "content": ai_response})

    # Save conversation history to the session
    request.session['conv_history'] = conv_history

    return JsonResponse({'message': ai_response})

# Constructs the request to the Open AI API using the conversation history
# and returns the API's response
def query_gpt4(messages):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4-1106-preview",
        "messages": messages,
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        response_json = response.json()
        # Log the entire response
        print("Response JSON from OpenAI:", response_json)

        # Now, check if 'choices' key is in the response
        if 'choices' in response_json:
            return response_json['choices'][0]['message']['content']
        else:
            # If 'choices' isn't present, log an error and return a default message
            print("Error: 'choices' key not in response JSON from OpenAI.")
            return "Sorry, I can't process that right now."
    else:
        # If the response wasn't successful, log the status code and response text
        print(f"Error: Received status code {response.status_code}")
        print("Response text:", response.text)
        return "Sorry, I can't process that right now."
