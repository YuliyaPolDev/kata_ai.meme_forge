"""Example of sending an image to DIAL for recognition using GPT-4o."""
import os
import base64
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()

# Replace `image.png` with your real image file path:
with open("image.png", "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2025-04-01-preview",
    azure_endpoint="https://ai-proxy.lab.epam.com/"
)

# Create the chat completion request
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What is on image?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    }
                }
            ]
        }
    ]
)

print(response.choices[0].message.content)
