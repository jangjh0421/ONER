import base64
import requests

api_key = "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"


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


user_input = input("User: ")

# Getting the base64 string
base64_image = encode_image(user_input)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What’s in this image? Try to come up with a analytical point of view as much as possible -- like an art concierge or a art professor"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 1000
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
res_json = response.json()

print(res_json['choices'][0]['message']['content'])
