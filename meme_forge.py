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
    def overlay_text_on_image(self, image_path, meme_text):
        """Overlay meme text (top and bottom) on the image in classic meme style."""
        from PIL import Image, ImageDraw, ImageFont
        # Parse meme_text: expect two lines separated by '---'
        if '---' in meme_text:
            top_text, bottom_text = [line.strip() for line in meme_text.split('---', 1)]
        else:
            # fallback: try to split by newline or just use as top
            lines = meme_text.splitlines()
            top_text = lines[0] if lines else meme_text
            bottom_text = lines[1] if len(lines) > 1 else ''

        # Open image
        img = Image.open(image_path).convert('RGB')
        draw = ImageDraw.Draw(img)
        width, height = img.size

        # Try to use Impact or fallback to default
        try:
            font_path = "C:/Windows/Fonts/impact.ttf" if os.name == 'nt' else "/usr/share/fonts/truetype/impact.ttf"
            font = ImageFont.truetype(font_path, size=int(height/11))
        except Exception:
            font = ImageFont.truetype(font=None, size=int(height/11)) if hasattr(ImageFont, 'truetype') else ImageFont.load_default()

        # Helper to measure text size (Pillow >=10.0.0 uses textbbox)
        def get_text_size(text, font):
            text = text.upper()
            try:
                bbox = draw.textbbox((0, 0), text, font=font)
                w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            except AttributeError:
                w, h = draw.textsize(text, font=font)
            return w, h

        # Dynamically fit font size to image width
        def fit_font(texts, max_width, initial_size):
            size = initial_size
            while size > 10:
                try:
                    font_path = "C:/Windows/Fonts/impact.ttf" if os.name == 'nt' else "/usr/share/fonts/truetype/impact.ttf"
                    font = ImageFont.truetype(font_path, size=size)
                except Exception:
                    font = ImageFont.truetype(font=None, size=size) if hasattr(ImageFont, 'truetype') else ImageFont.load_default()
                if all(get_text_size(t, font)[0] <= max_width for t in texts):
                    return font
                size -= 2
            return font

        # Arrange both lines at the top, with padding
        lines = [top_text]
        if bottom_text:
            lines.append(bottom_text)
        padding = int(height * 0.03)
        line_spacing = int(height * 0.01)
        max_text_width = int(width * 0.95)
        font = fit_font(lines, max_text_width, int(height/11))

        # Optionally, add a semi-transparent rectangle for readability
        total_text_height = sum(get_text_size(line, font)[1] for line in lines) + (len(lines)-1)*line_spacing + 2*padding
        rect_height = total_text_height
        rect = Image.new('RGBA', (width, rect_height), (0,0,0,120))
        img_rgba = img.convert('RGBA')
        img_rgba.paste(rect, (0,0), rect)
        draw = ImageDraw.Draw(img_rgba)

        # Helper to draw outlined text
        def draw_text(text, y, font, outline=2):
            text = text.upper()
            w, h = get_text_size(text, font)
            x = (width - w) / 2
            # Draw outline
            for dx in range(-outline, outline+1):
                for dy in range(-outline, outline+1):
                    if dx != 0 or dy != 0:
                        draw.text((x+dx, y+dy), text, font=font, fill='black')
            # Draw main text
            draw.text((x, y), text, font=font, fill='white')

        # Draw both lines at the top
        y = padding
        for line in lines:
            draw_text(line, y, font)
            y += get_text_size(line, font)[1] + line_spacing

        # Save image (overwrite original)
        img_final = img_rgba.convert('RGB')
        img_final.save(image_path)
        return image_path
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
        """Generate meme text in strict two-line format for workplace humor"""
        prompt = f'''
You are a professional meme creator specializing in workplace humor. Create meme text for this situation: "{situation_description}"
Format requirements:
- Return ONLY two lines separated by ---
- First line: setup/situation (1 line, concise)
- Second line: punchline/funny twist (1 line, humorous)
- Use classic meme style and internet culture references
- Make it relatable for office workers
- Maximum 40 characters per line
Examples:
Input: "deadline moved up"
Output: When the deadline was tomorrow---
But now it's in 30 minutes
Input: "too many meetings"
Output: Another meeting that could've been---
an email
'''
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
                max_tokens=100
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating meme text: {e}")
            return None
    
    def generate_meme_image(self, situation_description, meme_text):
        """Generate meme image using DALL-E-3"""
        # Create detailed cartoon/animation style meme prompt
        if '---' in meme_text:
            top_text = meme_text.split('---')[0].strip()
            bottom_text = meme_text.split('---')[1].strip()
        else:
            lines = meme_text.splitlines()
            top_text = lines[0] if lines else ''
            bottom_text = lines[1] if len(lines) > 1 else ''

        image_prompt = f'''
You are a professional meme creator specializing in workplace humor.
Create a static meme image in a cartoon/animation style for this situation: "{situation_description}"
Format requirements:
Return only one image (no text explanation)
Style: bright, colorful, cartoonish, exaggerated expressions (Simpsons-inspired)
Include two lines of text on the image, in classic meme format:
Top text: setup/situation (concise, max 40 characters)
Bottom text: punchline/funny twist (max 40 characters)
Use Impact font, bold white text with black outline
Scene should depict a funny office or workplace scenario (e.g. cubicles, coworkers, meetings, coffee, deadlines)
Humor should be relatable, clever, and PG-rated
Facial expressions and body language should enhance the joke
Meme text context:
Top text: {top_text}
Bottom text: {bottom_text}
'''
        
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
        """Complete meme creation pipeline with text overlay"""
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
        if not filepath:
            print("❌ Failed to download meme")
            return None
        # Step 4: Overlay text on image
        print("✍️  Adding text to meme image...")
        self.overlay_text_on_image(filepath, meme_text)
        print("✅ Meme creation complete!")
        return {
            "text": meme_text,
            "image_path": filepath,
            "situation": situation_description
        }


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