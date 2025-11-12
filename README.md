# Meme Forge MVP 🔥

AI-powered workplace meme generator that combines LLM text generation with DALL-E image generation.

## Features

- **Terminal-based interface**: No UI needed, works directly in VS Code terminal
- **LLM + DALL-E integration**: Uses both text generation (GPT-4o) and image generation (DALL-E-3)
- **Workplace-focused**: Generates relatable office/work situation memes
- **File organization**: Saves generated memes to `static/generated`
- **Batch processing**: Can generate multiple memes from predefined situations
- **Image viewing**: Built-in utility to view generated memes

## Setup

1. **Install dependencies**:
   ```bash
   python setup.py
   ```

2. **Configure API Key**: 
   - Update the `.env` file with your actual DIAL API key
   - Replace "XXX" with your real API key

## Usage

### Interactive Mode
Generate memes one at a time:
```bash
python meme_forge.py
```

### Batch Generation
Generate multiple memes from predefined workplace situations:
```bash
python batch_meme_generator.py
```

### View Generated Memes
View and list generated memes:
```bash
python view_memes.py
```

## File Structure

```
├── meme_forge.py           # Main meme generation engine
├── batch_meme_generator.py # Batch processing script
├── view_memes.py          # Meme viewer utility
├── setup.py               # Setup script
├── .env                   # Environment variables (API key)
├── requirements.txt       # Python dependencies
├── static/
│   ├── generated/         # Generated memes storage
│   └── uploads/          # File uploads (if needed)
└── templates/            # Template files (if needed)
```

## Example Usage

1. Describe a work situation: "When you fix a bug but create three new ones"
2. The system generates funny meme text
3. Creates a workplace-themed image using DALL-E
4. Saves the complete meme to `static/generated/`

## API Integration

Uses DIAL API for:
- **Text Generation**: GPT-4o for witty workplace meme text
- **Image Generation**: DALL-E-3 for workplace-themed meme images

## Requirements

- Python 3.8+
- DIAL API key
- Internet connection for API calls
