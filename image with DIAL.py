"""Example of generating an image using Azure OpenAI DALL·E-3 model"""

# Place your DIAL API key to .env file as AZURE_OPENAI_API_KEY=dial...

import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

# Model:
deployment_model="dall-e-3"

# Standard setting:
api_version="2025-04-01-preview"
headers = {
    "api-key": os.environ["AZURE_OPENAI_API_KEY"],
    "Content-Type": "application/json"
}
payload = {
    "messages": [
        {
            "role": "user",
            "content": "Generate an image of a cat with a hat on a beach"
        }
    ],
}
#### Generate image: ####

response = requests.post(
    f"https://ai-proxy.lab.epam.com/openai/deployments/{deployment_model}/chat/completions?api-version={api_version}",
    headers=headers,
    json=payload
).json()

image_data = response["choices"][0]["message"]["custom_content"]['attachments']
print(json.dumps(image_data, indent=3))

image_url = ""
for item in image_data:
    if item['title'] == 'Revised prompt':
        print("Revised prompt:", item['data'])
    elif item['title'] == 'Image':
        image_url = item['url']

print("Image URL:", image_url)

### Download the image: ###

url = f"https://ai-proxy.lab.epam.com/v1/{image_url}"

# Download the file:
response = requests.get(url, headers={"Api-Key": os.environ["AZURE_OPENAI_API_KEY"]})
response.raise_for_status()  # fail if not success

# Remove image from the DIAL server after download
delete_response = requests.delete(url, headers={"Api-Key": os.environ["AZURE_OPENAI_API_KEY"]})
delete_response.raise_for_status()

# You can save it to the file:
with open("generated_image.png", "wb") as f:
    f.write(response.content)

# # or directly load and show it with pillow:
# from PIL import Image
# from io import BytesIO
# img = Image.open(BytesIO(response.content))
# img.show()

####  You can pass some configuration (quality, size or style) to the deployment too, check available parameters: ####

# deployment_model = "dall-e-3"
# headers = {
#     "Api-Key": os.environ["AZURE_OPENAI_API_KEY"],
#     # "Content-Type": "application/json"
# }
# response = requests.get(
#     f"https://ai-proxy.lab.epam.com/v1/deployments/{deployment_model}/configuration",
#     headers=headers
# ).json()

# print(json.dumps(response, indent=3))