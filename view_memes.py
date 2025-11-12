"""
Simple meme viewer utility
"""
import os
import json
from PIL import Image

def view_latest_meme():
    """View the most recently generated meme"""
    
    generated_dir = "static/generated"
    
    if not os.path.exists(generated_dir):
        print("No memes generated yet!")
        return
    
    # Find most recent PNG file
    png_files = [f for f in os.listdir(generated_dir) if f.endswith('.png')]
    
    if not png_files:
        print("No meme images found!")
        return
    
    # Sort by modification time
    png_files.sort(key=lambda x: os.path.getmtime(os.path.join(generated_dir, x)), reverse=True)
    latest_meme = png_files[0]
    
    try:
        img_path = os.path.join(generated_dir, latest_meme)
        img = Image.open(img_path)
        img.show()
        print(f"Showing: {latest_meme}")
        
    except Exception as e:
        print(f"Error viewing image: {e}")

def list_all_memes():
    """List all generated memes"""
    
    generated_dir = "static/generated"
    
    if not os.path.exists(generated_dir):
        print("No memes generated yet!")
        return
    
    png_files = [f for f in os.listdir(generated_dir) if f.endswith('.png')]
    
    if not png_files:
        print("No meme images found!")
        return
    
    print("Generated memes:")
    print("=" * 40)
    
    for i, filename in enumerate(sorted(png_files), 1):
        filepath = os.path.join(generated_dir, filename)
        size = os.path.getsize(filepath)
        print(f"{i}. {filename} ({size} bytes)")
    
    # Show summary if available
    summary_path = os.path.join(generated_dir, "batch_summary.json")
    if os.path.exists(summary_path):
        with open(summary_path) as f:
            summary = json.load(f)
        print(f"\nBatch summary: {summary['total_generated']} memes generated")

def main():
    """Main viewer interface"""
    
    while True:
        print("\n🖼️  Meme Viewer")
        print("1. View latest meme")
        print("2. List all memes") 
        print("3. Quit")
        
        choice = input("Choose option (1-3): ").strip()
        
        if choice == "1":
            view_latest_meme()
        elif choice == "2":
            list_all_memes()
        elif choice == "3":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()