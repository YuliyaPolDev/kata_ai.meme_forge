"""
Meme Forge MVP - AI-powered workplace meme generator
Uses Perplexity API for text generation
Uses Clipdrop API (Stable Diffusion) for image generation
"""
import os
import requests
import base64
from dotenv import load_dotenv
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

load_dotenv()

class MemeForge:
    def __init__(self):
        # Perplexity API for text generation
        self.perplexity_api_key = os.environ.get("PERPLEXITY_API_KEY")
        self.perplexity_url = "https://api.perplexity.ai/chat/completions"
        
        # --- CORRECTED Clipdrop API ---
        self.clipdrop_api_key = os.environ.get("CLIPDROP_API_KEY")
        # --- CORRECTED URL (from clipdrop-api.co) ---
        self.clipdrop_url = "https://clipdrop-api.co/text-to-image/v1"
        
        if not self.perplexity_api_key:
            print("⚠️  Error: PERPLEXITY_API_KEY not set in .env")
        else:
            print("✅ Perplexity API Key loaded")
        
        if not self.clipdrop_api_key:
            print("⚠️  Error: CLIPDROP_API_KEY not set in .env")
            print("   (Get a free key from https://clipdrop.co/platform)")
        else:
            print("✅ Clipdrop API Key loaded")
    
    def generate_meme_text(self, situation_description, style="cartoon/animation", mood="funny"):
        """Generate meme text using Perplexity API"""
        
        prompt = f'''You are a professional meme creator specializing in workplace humor. Create meme text for this situation: "{situation_description}"
Style: {style}
Mood: {mood}

Format requirements:
- Return ONLY two lines separated by ---
- First line: setup/situation (1 line, concise, max 40 chars)
- Second line: punchline/funny twist (1 line, humorous, max 40 chars)
- Use classic meme style and internet culture references
- Make it relatable for office workers
- Be creative and funny

Example format:
Line 1---
Line 2

Create the meme text now:'''

        try:
            payload = {
                "model": "sonar-pro",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 150,
                "temperature": 0.8
            }
            
            headers = {
                "Authorization": f"Bearer {self.perplexity_api_key}",
                "Content-Type": "application/json"
            }
            
            print(f"📡 Sending request to Perplexity API...")
            
            response = requests.post(
                self.perplexity_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            print(f"Response status: {response.status_code}")
            
            response.raise_for_status()
            
            data = response.json()
            meme_text = data['choices'][0]['message']['content'].strip()
            
            # Ensure format has --- separator
            if '---' not in meme_text:
                lines = meme_text.split('\n')
                if len(lines) >= 2:
                    meme_text = f"{lines[0].strip()}---{lines[1].strip()}"
                else:
                    meme_text = f"{meme_text}---Generated meme"
            
            return meme_text
            
        except Exception as e:
            print(f"Error generating meme text: {e}")
            return None

    # --- CORRECTED FUNCTION (using new URL and form data) ---
    def generate_meme_image_with_text(self, situation_description, meme_text, style="cartoon/animation", mood="funny"):
        """
        Generate meme image using Clipdrop (Stable Diffusion) API.
        Falls back to a simple gradient if the API call fails.
        """
        
        print("🖼️  Attempting to generate image with Clipdrop (Free API)...")
        
        if not self.clipdrop_api_key:
            print("⚠️  CLIPDROP_API_KEY not set.")
            print("🎨 Falling back to simple gradient image.")
            return self.create_simple_meme_image(situation_description, meme_text, style, mood)

        # Clipdrop uses a simple API key in the header
        headers = {
            "x-api-key": self.clipdrop_api_key
        }
        
        image_prompt = f"a {mood} {style} image, meme background, {situation_description}"
        
        # --- CORRECTED form_data (removed aspect_ratio) ---
        # Clipdrop uses 'multipart/form-data' for its request
        form_data = {
            "prompt": (None, image_prompt)
        }

        try:
            response = requests.post(
                self.clipdrop_url, # Using the corrected URL
                headers=headers,
                files=form_data, # Use 'files' for multipart/form-data
                timeout=60 
            )
            
            print(f"Clipdrop response status: {response.status_code}")
            
            # Check for JSON error response
            if response.headers.get('Content-Type') == 'application/json':
                error_data = response.json()
                raise Exception(f"Clipdrop API error: {error_data.get('error', response.text)}")
            
            # Raise errors for 4xx/5xx if not JSON
            response.raise_for_status()
            
            # Success: response is 'image/png'
            img_data = response.content
            
            # Check for credits
            remaining = response.headers.get('x-remaining-credits')
            consumed = response.headers.get('x-credits-consumed')
            if remaining:
                print(f"✅ Image data received. Credits consumed: {consumed}. Credits remaining: {remaining}.")
            else:
                print("✅ Image data received from Clipdrop.")

            # Create a PIL image from the bytes
            img = Image.open(BytesIO(img_data))
            
            # Now, overlay the text
            print("🖌️  Overlaying text on Clipdrop image...")
            img_with_text = self.overlay_text_on_image_pil(img, meme_text)
            
            return img_with_text

        except Exception as e:
            print(f"❌ Error generating image with Clipdrop: {e}")
            print("🎨 Falling back to simple gradient image.")
            return self.create_simple_meme_image(situation_description, meme_text, style, mood)

    def overlay_text_on_image_pil(self, img, meme_text):
        """Overlay meme text on generated image"""
        
        # Parse text
        if '---' in meme_text:
            top_text = meme_text.split('---')[0].strip()
            bottom_text = meme_text.split('---')[1].strip()
        else:
            lines = meme_text.splitlines()
            top_text = lines[0] if lines else ''
            bottom_text = lines[1] if len(lines) > 1 else ''
        
        width, height = img.size
        draw = ImageDraw.Draw(img)
        
        # Load font
        try:
            # Tip: Bundle "impact.ttf" with your app for more reliability
            font_path = "C:/Windows/Fonts/impact.ttf" if os.name == 'nt' else "/usr/share/fonts/truetype/impact.ttf"
            font = ImageFont.truetype(font_path, size=int(height/10))
        except Exception:
            print("⚠️ Impact font not found, using default font.")
            font = ImageFont.load_default()
        
        # Helper function to draw text with outline
        def draw_outlined_text(draw, text, x, y, font, fill='white', outline='black'):
            text = text.upper()
            # Draw outline
            for dx in [-2, -1, 0, 1, 2]:
                for dy in [-2, -1, 0, 1, 2]:
                    if dx != 0 or dy != 0:
                        draw.text((x+dx, y+dy), text, font=font, fill=outline)
            # Draw main text
            draw.text((x, y), text, font=font, fill=fill)
        
        # Get text dimensions
        def get_text_bbox(text, font):
            if hasattr(font, "getbbox"):
                return font.getbbox(text)
            else:
                return draw.textbbox((0, 0), text, font=font)
        
        # Draw top text
        if top_text:
            bbox = get_text_bbox(top_text.upper(), font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw_outlined_text(draw, top_text, x, 20, font)
        
        # Draw bottom text
        if bottom_text:
            bbox = get_text_bbox(bottom_text.upper(), font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (width - text_width) // 2
            y = height - text_height - 20 - (bbox[1]) # Adjust for font bounding box
            draw_outlined_text(draw, bottom_text, x, y, font)
        
        return img

    def create_simple_meme_image(self, situation_description, meme_text, style="cartoon/animation", mood="funny"):
        """Fallback: Create a simple meme image with gradient background"""
        
        # Use 1024x1024 to match the API's default fallback
        width, height = 1024, 1024
        
        # Color schemes based on style
        color_schemes = {
            "cartoon/animation": {
                "start": (100, 150, 255),
                "end": (150, 100, 255)
            },
            "realistic": {
                "start": (200, 200, 200),
                "end": (150, 150, 150)
            },
            "meme-style": {
                "start": (255, 200, 0),
                "end": (255, 150, 0)
            }
        }
        
        colors = color_schemes.get(style, color_schemes["cartoon/animation"])
        
        # Create gradient
        img = Image.new('RGB', (width, height), colors["start"])
        draw = ImageDraw.Draw(img)
        
        for y in range(height):
            ratio = y / height
            r = int(colors["start"][0] * (1 - ratio) + colors["end"][0] * ratio)
            g = int(colors["start"][1] * (1 - ratio) + colors["end"][1] * ratio)
            b = int(colors["start"][2] * (1 - ratio) + colors["end"][2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Overlay text
        img = self.overlay_text_on_image_pil(img, meme_text)
        
        return img

    def save_image(self, img, filename=None):
        """Save image to file"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"meme_{timestamp}.png"
        
        try:
            os.makedirs("static/generated", exist_ok=True)
            filepath = os.path.join("static/generated", filename)
            
            img.save(filepath)
            
            print(f"💾 Meme saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error saving image: {e}")
            return None

    def create_meme(self, situation_description, style="cartoon/animation", mood="funny"):
        """Complete meme creation pipeline"""
        print(f"🎨 Creating meme for: '{situation_description}'")
        print("=" * 50)
        
        # Step 1: Generate text using Perplexity
        print("📝 Generating meme text with Perplexity...")
        meme_text = self.generate_meme_text(situation_description, style=style, mood=mood)
        if not meme_text:
            print("❌ Failed to generate meme text")
            return None
        print("✅ Meme text generated:")
        print(meme_text)
        print()
        
        # Step 2: Generate image using Clipdrop
        print("🖼️  Generating meme image...")
        img = self.generate_meme_image_with_text(situation_description, meme_text, style=style, mood=mood)
        if not img:
            print("❌ Failed to create meme image")
            return None
        print("✅ Meme image created")
        
        # Step 3: Save image
        print("💾 Saving meme...")
        filepath = self.save_image(img)
        if not filepath:
            print("❌ Failed to save meme")
            return None
        
        print("✅ Meme creation complete!")
        return {
            "text": meme_text,
            "image_path": filepath,
            "situation": situation_description,
            "style": style,
            "mood": mood
        }


def main():
    """Main CLI interface"""
    print("🔥 Welcome to Meme Forge MVP! 🔥")
    print("AI-powered workplace meme generator")
    print("Using Perplexity API for text + Clipdrop API for images")
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

        style = input("Enter meme style (cartoon/animation, realistic, meme-style): ").strip()
        if not style:
            style = "cartoon/animation"
        mood = input("Enter meme mood (funny, sarcastic, dramatic): ").strip()
        if not mood:
            mood = "funny"

        try:
            result = forge.create_meme(situation, style=style, mood=mood)
            if result:
                print(f"\n🎉 Your meme is ready!")
                print(f"Text: {result['text']}")
                print(f"Image saved to: {result['image_path']}")
        except Exception as e:
            print(f"Error creating meme: {e}")

        print("\n" + "=" * 50)


if __name__ == "__main__":
    main()