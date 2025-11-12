"""
Simple meme generation test and viewer
"""
import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def generate_test_meme():
    """Generate a simple test meme to demonstrate viewing"""
    
    # DIAL API configuration
    api_key = os.environ["AZURE_OPENAI_API_KEY"]
    base_url = "https://ai-proxy.lab.epam.com"
    api_version = "2025-04-01-preview"
    
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }
    
    # Simple workplace meme prompt
    payload = {
        "messages": [
            {
                "role": "user",
                "content": "Create a funny workplace meme image about 'When you fix a bug but create three new ones'. Make it a classic meme format with a confused or frustrated person in an office setting."
            }
        ],
    }
    
    print("🎨 Generating test meme...")
    
    try:
        # Generate image using DALL-E-3
        response = requests.post(
            f"{base_url}/openai/deployments/dall-e-3/chat/completions?api-version={api_version}",
            headers=headers,
            json=payload
        ).json()
        
        if "choices" not in response:
            print("❌ Error in image generation:", response)
            return None
        
        image_data = response["choices"][0]["message"]["custom_content"]['attachments']
        
        image_url = ""
        revised_prompt = ""
        
        for item in image_data:
            if item['title'] == 'Revised prompt':
                revised_prompt = item['data']
            elif item['title'] == 'Image':
                image_url = item['url']
        
        print(f"✅ Image generated!")
        print(f"Revised prompt: {revised_prompt}")
        
        # Download the image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_meme_{timestamp}.png"
        
        url = f"{base_url}/v1/{image_url}"
        
        # Download the file
        response = requests.get(url, headers={"Api-Key": api_key})
        response.raise_for_status()
        
        # Save to static/generated/ directory
        os.makedirs("static/generated", exist_ok=True)
        filepath = os.path.join("static/generated", filename)
        
        with open(filepath, "wb") as f:
            f.write(response.content)
        
        # Clean up from DIAL server
        delete_response = requests.delete(url, headers={"Api-Key": api_key})
        delete_response.raise_for_status()
        
        print(f"💾 Meme saved to: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def view_meme_with_system_viewer(filepath):
    """Open meme with system default image viewer"""
    import subprocess
    import platform
    
    try:
        if platform.system() == "Windows":
            os.startfile(filepath)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", filepath])
        else:  # Linux
            subprocess.run(["xdg-open", filepath])
        
        print(f"🖼️  Opened {filepath} with system viewer")
        
    except Exception as e:
        print(f"❌ Error opening image: {e}")

def view_meme_with_pillow(filepath):
    """Open meme with Pillow (Python imaging library)"""
    try:
        from PIL import Image
        img = Image.open(filepath)
        img.show()
        print(f"🖼️  Opened {filepath} with Pillow viewer")
        
    except ImportError:
        print("❌ Pillow not available. Install with: pip install Pillow")
    except Exception as e:
        print(f"❌ Error opening image: {e}")

def main():
    """Main test function"""
    print("🔥 Meme Generation & Viewing Test 🔥")
    print("=" * 40)
    
    # Generate test meme
    filepath = generate_test_meme()
    
    if filepath and os.path.exists(filepath):
        print(f"\n✅ Test meme created successfully!")
        print(f"Location: {filepath}")
        
        print("\n🖼️  Viewing options:")
        print("1. Opening with system default viewer...")
        view_meme_with_system_viewer(filepath)
        
        print("2. You can also use Pillow to view in Python:")
        view_meme_with_pillow(filepath)
        
        print("\n📁 File Explorer:")
        print(f"You can also manually open: {os.path.abspath(filepath)}")
        
    else:
        print("❌ Failed to generate test meme")

if __name__ == "__main__":
    main()