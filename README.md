
# Meme Forge MVP 🔥

AI-powered workplace meme generator for the workplace, combining GPT-4o text with DALL-E-3 images. Generate, batch, and view memes right from your terminal!

---

## 📝 Project Summary

Meme Forge is a terminal-based Python tool that creates workplace memes using the latest AI models. It generates meme text with GPT-4o and images with DALL-E-3, saving results for easy viewing and sharing.

---


## 🚀 Features

- 🖥️ **Terminal-based interface**: No UI needed, works directly in VS Code or any terminal
- 🤖 **LLM + DALL-E integration**: GPT-4o for text, DALL-E-3 for images
- 🏢 **Workplace-focused**: Generates relatable office/work situation memes
- 📂 **Organized output**: Saves memes to `static/generated/`
- 📦 **Batch processing**: Generate multiple memes from a list
- 🖼️ **Image viewing**: Built-in meme viewer utility
- 🧪 **Test meme generation**: Quickly test meme creation and viewing with `test_meme_generation.py`
- 🖼️ **Image recognition**: Recognize content in images using GPT-4o with `image recog.py`
- 🎨 **Direct DALL-E image generation**: Generate images with custom prompts using `image with DIAL.py`

---

## ⚙️ Setup

1. **Install dependencies**
   - Open PowerShell or your terminal in the project folder.
   - Run:
     ```powershell
     python setup.py
     ```

2. **Configure API Key**
   - Open the `.env` file in the project root.
   - Replace `XXX` with your actual DIAL API key:
     ```env
     AZURE_OPENAI_API_KEY=your_actual_api_key_here
     ```

---

## 💡 Usage


### Interactive Meme Generation

Generate memes one at a time:
```powershell
python meme_forge.py
```

### Batch Meme Generation

Generate memes for a set of predefined workplace situations:
```powershell
python batch_meme_generator.py
```

### View Generated Memes

Menu-driven meme viewer:
```powershell
python view_memes.py
```

### Test Meme Generation & Viewing

# Meme Forge MVP 🔥

AI-powered workplace meme generator for the workplace, combining GPT-4o text with DALL-E-3 images. Generate, batch, and view memes right from your terminal!

---

## 📝 Project Summary

Meme Forge is a terminal-based Python tool that creates workplace memes using the latest AI models. It generates meme text with GPT-4o and images with DALL-E-3, saving results for easy viewing and sharing.

---

## 🚀 Features

- 🖥️ **Terminal-based interface**: No UI needed, works directly in VS Code or any terminal
- 🤖 **LLM + DALL-E integration**: GPT-4o for text, DALL-E-3 for images
- 🏢 **Workplace-focused**: Generates relatable office/work situation memes
- 📂 **Organized output**: Saves memes to `static/generated/`
- 📦 **Batch processing**: Generate multiple memes from a list
- 🖼️ **Image viewing**: Built-in meme viewer utility
- 🧪 **Test meme generation**: Quickly test meme creation and viewing with `test_meme_generation.py`
- 🖼️ **Image recognition**: Recognize content in images using GPT-4o with `image recog.py`
- 🎨 **Direct DALL-E image generation**: Generate images with custom prompts using `image with DIAL.py`
- ✍️ **Classic meme text overlay**: Automatically overlays generated text on images in classic meme style

---

## ⚙️ Setup

1. **Install dependencies**
   - Open PowerShell or your terminal in the project folder.
   - Run:
     ```powershell
     python setup.py
     ```

2. **Configure API Key**
   - Open the `.env` file in the project root.
   - Replace `XXX` with your actual DIAL API key:
     ```env
     AZURE_OPENAI_API_KEY=your_actual_api_key_here
     ```

---

## 💡 Usage

### Interactive Meme Generation

Generate memes one at a time:
```powershell
python meme_forge.py
```

### Batch Meme Generation

Generate memes for a set of predefined workplace situations:
```powershell
python batch_meme_generator.py
```

### View Generated Memes

Menu-driven meme viewer:
```powershell
python view_memes.py
```

### Test Meme Generation & Viewing

Quickly test meme creation and open the result:
```powershell
python test_meme_generation.py
```

### Image Recognition (GPT-4o Vision)

Recognize content in an image using GPT-4o:
```powershell
python "image recog.py"
# (edit the script to specify your image file)
```

### Generate Image with DALL-E-3 Directly

Generate an image with a custom prompt:
```powershell
python "image with DIAL.py"
# (edit the script to specify your prompt)
```

---

## 📁 File Structure

```
├── meme_forge.py               # Main meme generation engine
├── batch_meme_generator.py     # Batch meme generator
├── view_memes.py               # Meme viewer utility
├── test_meme_generation.py     # Quick test for meme creation/viewing
├── image recog.py              # Image recognition with GPT-4o
├── image with DIAL.py          # Direct DALL-E-3 image generation
├── setup.py                    # Setup script
├── .env                        # API key config
├── requirements.txt            # Python dependencies
├── static/
│   ├── generated/              # Generated memes
│   └── uploads/                # (Optional) uploads
├── templates/                  # (Optional) templates
├── app/                        # (Reserved for future web app, currently empty)
├── HOW_TO_VIEW_MEMES.md        # Viewing instructions
└── __pycache__/                # Python bytecode cache (auto-generated)
```

> **Note:**
> - The `uploads/` and `templates/` folders are optional and may be empty.
> - The `app/` folder is reserved for future expansion (e.g., web interface).

---

## 🖼️ Viewing Memes

- All memes are saved as `.png` files in `static/generated/`.
- Use the built-in viewer (`python view_memes.py`), open in VS Code, or double-click in your OS file explorer.
- See [HOW_TO_VIEW_MEMES.md](HOW_TO_VIEW_MEMES.md) for more tips.

---

## 📝 Example Workflow

1. **Describe a work situation**:  
   _"When you fix a bug but create three new ones"_
2. **System generates meme text**:  
   _Setup and punchline in classic meme style._
3. **Creates a workplace-themed image** using DALL-E-3.
4. **Saves the meme** to `static/generated/`.
5. **Overlays the generated text** on the image in classic meme style.

---

## 🌐 API Integration

- **Text Generation**: GPT-4o via DIAL API
- **Image Generation**: DALL-E-3 via DIAL API

---

## 📦 Requirements

- Python 3.8 or higher
- DIAL API key (set in `.env` as `AZURE_OPENAI_API_KEY`)
- Internet connection
- All dependencies from `requirements.txt` (install with `pip install -r requirements.txt`)

---

## 🛠️ Troubleshooting

- **No memes generated?**
  - Check your API key in `.env` (should be `AZURE_OPENAI_API_KEY=your_actual_api_key_here`)
  - Ensure internet connectivity
  - Make sure your `.env` file is in the project root and not named `.env.txt`
  - If you see errors about missing dependencies, run: `pip install -r requirements.txt`
- **Viewer not working?**
  - Install Pillow: `pip install Pillow`
  - Open images manually in your OS or VS Code
  - On Windows, you can use `start static\generated\meme_filename.png` in PowerShell
- **Permission or file not found errors?**
  - Ensure the `static/generated/` directory exists (it will be created automatically if needed)
  - Check that your antivirus or security software is not blocking file creation
- **API errors or timeouts?**
  - Verify your API key is valid and not expired
  - Try again later in case of temporary network issues

---

## 📚 More Info

- See [HOW_TO_VIEW_MEMES.md](HOW_TO_VIEW_MEMES.md) for detailed viewing instructions.
- For batch results, check `static/generated/batch_summary.json`.

---

## 🤝 Contributing

Pull requests and suggestions are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

MIT License (see `LICENSE` file if present).

---

Enjoy creating workplace memes! 🎉
