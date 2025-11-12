"""
Setup script for Meme Forge MVP
"""
import os
import subprocess
import sys

def create_directories():
    """Create necessary directories"""
    
    dirs = [
        "static/generated",
        "static/uploads",
        "templates"
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Created directory: {dir_path}")

def check_env_file():
    """Check if .env file exists with API key"""
    
    if not os.path.exists(".env"):
        print("❌ .env file not found!")
        print("Creating .env template...")
        
        with open(".env", "w") as f:
            f.write("AZURE_OPENAI_API_KEY=XXX\n")
        
        print("✅ Created .env file")
        print("⚠️  Please replace 'XXX' with your actual DIAL API key in .env file")
        return False
    
    # Check if API key is set
    with open(".env") as f:
        content = f.read()
        if "XXX" in content:
            print("⚠️  Please replace 'XXX' with your actual DIAL API key in .env file")
            return False
    
    print("✅ .env file configured")
    return True

def install_requirements():
    """Install Python requirements"""
    
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return False
    
    try:
        print("📦 Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def main():
    """Main setup function"""
    
    print("🔧 Setting up Meme Forge MVP...")
    print("=" * 40)
    
    # Create directories
    create_directories()
    
    # Check environment
    env_ok = check_env_file()
    
    # Install requirements
    req_ok = install_requirements()
    
    print("\n" + "=" * 40)
    
    if env_ok and req_ok:
        print("🎉 Setup complete!")
        print("\nTo get started:")
        print("1. Make sure your DIAL API key is set in .env")
        print("2. Run: python meme_forge.py")
        print("3. Or try batch generation: python batch_meme_generator.py")
    else:
        print("⚠️  Setup incomplete. Please check the issues above.")

if __name__ == "__main__":
    main()