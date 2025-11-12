# 🖼️ How to View Generated Memes - Complete Guide

## 📍 Where Memes Are Stored
All generated memes are saved in:
```
static/generated/
```

## 🎯 Methods to View Generated Memes

### 1. **Built-in Meme Viewer (Recommended)**
```bash
python view_memes.py
```

**Features:**
- Menu-driven interface
- View latest meme
- List all generated memes
- Shows file sizes and creation dates

### 2. **Windows File Explorer**
- Navigate to: `C:\Users\YuliyaPalamarchuk\kata_ai_2025_meme\kata_ai.meme_forge\static\generated`
- Double-click any `.png` file to open with default image viewer

### 3. **VS Code Image Preview**
- In VS Code Explorer, navigate to `static/generated/`
- Click on any `.png` file to preview in VS Code
- VS Code has built-in image preview support

### 4. **Command Line (Windows)**
```powershell
# Open specific meme with default app
start static\generated\meme_filename.png

# Open the generated folder
start static\generated\

# List all memes
dir static\generated\*.png
```

### 5. **Using Python PIL (Pillow)**
```python
from PIL import Image
img = Image.open("static/generated/meme_filename.png")
img.show()
```

### 6. **Web Browser**
- Open any generated `.png` file directly in your web browser
- Drag and drop the file into browser window

## 📋 Quick Commands Reference

### Check if memes exist:
```bash
dir static\generated
```

### View latest meme info:
```bash
dir static\generated\*.png /O:D
```

### Open generated folder in Explorer:
```bash
explorer static\generated
```

## 🔧 Troubleshooting

### If no memes appear:
1. **Check API connection**: Ensure DIAL API is accessible
2. **Verify API key**: Check `.env` file has correct key
3. **Network issues**: Try again later if there are connectivity problems

### If viewer doesn't work:
1. **Install Pillow**: `pip install Pillow`
2. **Use File Explorer**: Manual navigation always works
3. **VS Code Preview**: Built-in image preview in editor

### File format:
- All memes are saved as `.png` files
- Filename format: `meme_YYYYMMDD_HHMMSS.png`
- Also includes batch summary: `batch_summary.json`

## 🎨 Example Workflow

1. **Generate memes**:
   ```bash
   python meme_forge.py
   # or
   python batch_meme_generator.py
   ```

2. **View immediately**:
   ```bash
   python view_memes.py
   ```

3. **Or check manually**:
   ```bash
   explorer static\generated
   ```

## 📊 Batch Generation Results

After running `batch_meme_generator.py`, you'll also get:
- `batch_summary.json` - Contains metadata about all generated memes
- Individual `.png` files for each successful generation
- Statistics on success/failure rates