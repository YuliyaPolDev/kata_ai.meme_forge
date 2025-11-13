from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from meme_forge import MemeForge
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize meme forge
forge = MemeForge()

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200

@app.route('/api/generate', methods=['POST'])
def generate_meme():
    """Generate a single meme"""
    data = request.json
    situation = data.get('situation')
    style = data.get('style', 'cartoon/animation')
    mood = data.get('mood', 'funny')
    
    if not situation:
        return jsonify({"error": "Situation required"}), 400
    
    try:
        result = forge.create_meme(situation, style=style, mood=mood)
        if result:
            return jsonify(result), 200
        return jsonify({"error": "Failed to generate meme"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/batch', methods=['POST'])
def batch_generate():
    """Generate multiple memes"""
    data = request.json
    situations = data.get('situations', [])
    
    results = []
    for situation in situations:
        try:
            result = forge.create_meme(situation)
            if result:
                results.append(result)
        except Exception as e:
            results.append({"error": str(e), "situation": situation})
    
    return jsonify({
        "total": len(situations),
        "generated": len([r for r in results if 'error' not in r]),
        "results": results
    }), 200

@app.route('/api/memes', methods=['GET'])
def list_memes():
    try:
        generated_dir = "static/generated"
        if not os.path.exists(generated_dir):
            return jsonify({"memes": []}), 200
        
        png_files = sorted(
            [f for f in os.listdir(generated_dir) if f.endswith('.png')],
            key=lambda x: os.path.getmtime(os.path.join(generated_dir, x)),
            reverse=True
        )
        
        memes = []
        for f in png_files:
            path = os.path.join(generated_dir, f)
            # Return the full path URL that Flask can serve
            memes.append({
                "filename": f,
                "url": f"/static/generated/{f}",  # This is the key!
                "size": os.path.getsize(path)
            })
        
        return jsonify({"memes": memes}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add this route to serve static files
@app.route('/static/generated/<filename>')
def serve_meme(filename):
    """Serve meme images"""
    return send_from_directory(os.path.join(os.getcwd(), 'static', 'generated'), filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)