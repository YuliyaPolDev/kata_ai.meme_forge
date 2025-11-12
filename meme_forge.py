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

import re

class MemeForge:
    @staticmethod
    def _sanitize_description(desc, maxlen=30):
        # Remove non-alphanumeric, replace spaces with underscores, truncate
        desc = desc.lower()
        desc = re.sub(r'[^a-z0-9\s]', '', desc)
        desc = re.sub(r'\s+', '_', desc)
        return desc[:maxlen].rstrip('_')

    @staticmethod
    def _get_next_seq_num(directory="static/generated"):  # returns int
        existing = [f for f in os.listdir(directory) if f.startswith("meme_") and f.endswith(".png")]
        nums = []
        for fname in existing:
            m = re.match(r"meme_(\d{3})_", fname)
            if m:
                nums.append(int(m.group(1)))
        return max(nums, default=0) + 1
    def overlay_text_on_image(self, image_path, meme_text):
        """Overlay meme text (top and bottom) on the image in classic meme style: top at top, bottom at bottom."""
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
                bbox = ImageDraw.Draw(img).textbbox((0, 0), text, font=font)
                w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            except AttributeError:
                w, h = ImageDraw.Draw(img).textsize(text, font=font)
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

        padding = int(height * 0.03)
        max_text_width = int(width * 0.95)
        font = fit_font([t for t in [top_text, bottom_text] if t], max_text_width, int(height/11))

        # Helper to draw outlined text
        def draw_text(draw, text, y, font, outline=2):
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

        img_rgba = img.convert('RGBA')
        draw = ImageDraw.Draw(img_rgba)

        # Draw top text at the top
        if top_text:
            y_top = padding
            draw_text(draw, top_text, y_top, font)

        # Draw bottom text at the bottom
        if bottom_text:
            _, h = get_text_size(bottom_text, font)
            y_bottom = height - h - padding
            draw_text(draw, bottom_text, y_bottom, font)

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
        # Load prompt templates from JSON file
        self.prompt_templates = self._load_prompt_templates()

    def _load_prompt_templates(self):
        """Load prompt templates from prompt_templates.json"""
        template_path = os.path.join(os.path.dirname(__file__), "prompt_templates.json")
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading prompt templates: {e}")
            # Fallback to hardcoded templates if file missing
            return {
                "text_prompt": {"template": "You are a professional meme creator specializing in workplace humor. Create meme text for this situation: '{situation_description}'\nStyle: {style}\nMood: {mood}\nFormat requirements:\n- Return ONLY two lines separated by ---\n- First line: setup/situation (1 line, concise)\n- Second line: punchline/funny twist (1 line, humorous)\n- Use classic meme style and internet culture references\n- Make it relatable for office workers\n- Maximum 40 characters per line\nExamples:\nInput: 'deadline moved up'\nOutput: When the deadline was tomorrow---\nBut now it's in 30 minutes\nInput: 'too many meetings'\nOutput: Another meeting that could've been---\nemail\n"},
                "image_prompt": {"template": "You are a professional meme creator specializing in workplace humor.\nCreate a static meme image in style: '{style}' for this situation: '{situation_description}' and in mood '{mood}'.\nFormat requirements:\n- Do NOT add any text to the image.\n- Depict a funny office or workplace scenario (e.g. cubicles, coworkers, meetings, coffee, deadlines) that visually represents the situation.\n- Humor should be relatable, clever, and PG-rated.\n- Facial expressions and body language should enhance the joke.\nExamples:\nInput: 'deadline moved up'\n→ Office worker panicking as a clock speeds up\nInput: 'too many meetings'\n→ Bored employee on an endless video call\n"}
            }
    
    def generate_meme_text(self, situation_description, style="cartoon/animation", mood="funny"):
        """Generate meme text in strict two-line format for workplace humor, using user-specified style and mood"""
        prompt_template = self.prompt_templates.get("text_prompt", {}).get("template", "")
        prompt = prompt_template.format(situation_description=situation_description, style=style, mood=mood)
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
    
    def generate_meme_image(self, situation_description, meme_text, style="cartoon/animation", mood="funny"):
        """Generate meme image using DALL-E-3 with user-specified style and mood, but instruct DALL-E to generate the scene ONLY, with NO text on the image. Text will be overlaid later."""
        image_prompt_template = self.prompt_templates.get("image_prompt", {}).get("template", "")
        image_prompt = image_prompt_template.format(situation_description=situation_description, style=style, mood=mood)
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": image_prompt
                }
            ],
        }
        try:
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
    
    def download_image(self, image_url, situation_description=None, filename=None):
        """Download generated image from DIAL, with custom filename if provided"""
        try:
            os.makedirs("static/generated", exist_ok=True)
            if not filename:
                # Use sequential numbering and sanitized description
                seq = self._get_next_seq_num()
                desc = self._sanitize_description(situation_description or "meme")
                filename = f"meme_{seq:03d}_{desc}.png"
            filepath = os.path.join("static/generated", filename)

            url = f"{self.base_url}/v1/{image_url}"
            response = requests.get(url, headers={"Api-Key": self.api_key})
            response.raise_for_status()
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
    
    def create_meme(self, situation_description, style="cartoon/animation", mood="funny"):
        """Complete meme creation pipeline with text overlay and user-specified style/mood"""
        print(f"🎨 Creating meme for: '{situation_description}'")
        print("=" * 50)
        print("📝 Generating meme text...")
        meme_text = self.generate_meme_text(situation_description, style=style, mood=mood)
        if not meme_text:
            print("❌ Failed to generate meme text")
            return None
        print("✅ Meme text generated:")
        print(meme_text)
        print()
        print("🖼️  Generating meme image...")
        image_url = self.generate_meme_image(situation_description, meme_text, style=style, mood=mood)
        if not image_url:
            print("❌ Failed to generate meme image")
            return None
        print("✅ Meme image generated")
        print("💾 Downloading meme...")
        filepath = self.download_image(image_url, situation_description=situation_description)
        if not filepath:
            print("❌ Failed to download meme")
            return None
        print("✍️  Adding text to meme image...")
        self.overlay_text_on_image(filepath, meme_text)
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

        style = input("Enter meme style (e.g. cartoon/animation, Simpsons-inspired, realistic): ").strip()
        if not style:
            style = "cartoon/animation"
        mood = input("Enter meme mood (e.g. funny, sarcastic, dramatic): ").strip()
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