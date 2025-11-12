"""
Meme Forge MVP - AI-powered workplace meme generator
Combines LLM text generation with DALL-E image generation
"""
import os
import json
import base64
import requests
from openai import AzureOpenAI
from dotenv import load_dotenv
from datetime import datetime

class MemeForge:
    def __init__(self):
        load_dotenv()
        
        # DIAL API configuration
        self.api_key = os.environ.get("AZURE_OPENAI_API_KEY", "XXX")
        self.base_url = "https://ai-proxy.lab.epam.com"
        self.api_version = "2025-04-01-preview"
        
        # Initialize Azure OpenAI client for text generation
        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.base_url
        )
        
        # Headers for DALL-E requests
        self.headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def generate_meme_text(self, situation_description):
        """Generate funny meme text based on work situation description"""
        
        prompt = f"""
        Create a funny, relatable workplace meme text based on this situation: "{situation_description}"

        Generate a meme in this format:
        - Top text (setup)
        - Bottom text (punchline)
        
        Make it witty, relatable for office workers, and appropriate for workplace sharing.
        Keep each line under 50 characters for better readability.
        
        Format your response as:
        TOP: [top text]
        BOTTOM: [bottom text]
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=150
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating meme text: {e}")
            return None
    
    def generate_meme_image(self, situation_description, meme_text):
        """Generate meme image using DALL-E-3"""
        
        # Create image prompt
        image_prompt = f"""
        Create a workplace meme image for this situation: "{situation_description}"
        
        The image should be:
        - Professional yet funny office/workplace themed
        - Suitable for adding text overlay later
        - Clean and simple composition
        - Appropriate for workplace sharing
        - In meme format style
        
        Meme text context: {meme_text}
        """
        
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": image_prompt
                }
            ],
        }
        
        try:
            # Generate image using DALL-E-3
            response = requests.post(
                f"{self.base_url}/openai/deployments/dall-e-3/chat/completions?api-version={self.api_version}",
                headers=self.headers,
                json=payload
            ).json()
            
            if "choices" not in response:
                print("Error in image generation response:", response)
                return None
            
            image_data = response["choices"][0]["message"]["custom_content"]['attachments']
            
            image_url = ""
            revised_prompt = ""
            
            for item in image_data:
                if item['title'] == 'Revised prompt':
                    revised_prompt = item['data']
                elif item['title'] == 'Image':
                    image_url = item['url']
            
            print(f"Revised prompt: {revised_prompt}")
            return image_url
            
        except Exception as e:
            print(f"Error generating meme image: {e}")
            return None
    
    def download_image(self, image_url, filename=None):
        """Download generated image from DIAL"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"meme_{timestamp}.png"
        
        try:
            url = f"{self.base_url}/v1/{image_url}"
            
            # Download the file
            response = requests.get(url, headers={"Api-Key": self.api_key})
            response.raise_for_status()
            
            # Save to static/generated/ directory
            os.makedirs("static/generated", exist_ok=True)
            filepath = os.path.join("static/generated", filename)
            
            with open(filepath, "wb") as f:
                f.write(response.content)
            
            # Clean up from DIAL server
            delete_response = requests.delete(url, headers={"Api-Key": self.api_key})
            delete_response.raise_for_status()
            
            print(f"Meme saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error downloading image: {e}")
            return None
    
    def create_meme(self, situation_description):
        """Complete meme creation pipeline"""
        
        print(f"🎨 Creating meme for: '{situation_description}'")
        print("=" * 50)
        
        # Step 1: Generate meme text
        print("📝 Generating meme text...")
        meme_text = self.generate_meme_text(situation_description)
        
        if not meme_text:
            print("❌ Failed to generate meme text")
            return None
        
        print("✅ Meme text generated:")
        print(meme_text)
        print()
        
        # Step 2: Generate image
        print("🖼️  Generating meme image...")
        image_url = self.generate_meme_image(situation_description, meme_text)
        
        if not image_url:
            print("❌ Failed to generate meme image")
            return None
        
        print("✅ Meme image generated")
        
        # Step 3: Download image
        print("💾 Downloading meme...")
        filepath = self.download_image(image_url)
        
        if filepath:
            print("✅ Meme creation complete!")
            return {
                "text": meme_text,
                "image_path": filepath,
                "situation": situation_description
            }
        else:
            print("❌ Failed to download meme")
            return None


def main():
    """Main CLI interface"""
    print("🔥 Welcome to Meme Forge MVP! 🔥")
    print("AI-powered workplace meme generator")
    print("=" * 40)
    
    forge = MemeForge()
    
    while True:
        print("\nDescribe your work situation for a meme:")
        print("(or type 'quit' to exit)")
        
        situation = input("Situation: ").strip()
        
        if situation.lower() in ['quit', 'exit', 'q']:
            print("Thanks for using Meme Forge! 👋")
            break
        
        if not situation:
            print("Please enter a situation description!")
            continue
        
        try:
            result = forge.create_meme(situation)
            
            if result:
                print(f"\n🎉 Your meme is ready!")
                print(f"Text: {result['text']}")
                print(f"Image saved to: {result['image_path']}")
            
        except Exception as e:
            print(f"Error creating meme: {e}")
        
        print("\n" + "=" * 50)


if __name__ == "__main__":
    main()