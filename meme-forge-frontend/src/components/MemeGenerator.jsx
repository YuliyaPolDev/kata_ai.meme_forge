import React, { useState } from 'react';
import { memeAPI } from '../services/api';
import './MemeGenerator.css';

export default function MemeGenerator() {
  const [situation, setSituation] = useState('');
  const [style, setStyle] = useState('cartoon/animation');
  const [mood, setMood] = useState('funny');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleGenerate = async (e) => {
    e.preventDefault();
    
    if (!situation.trim()) {
      setError('Please describe a situation');
      return;
    }
    
    setLoading(true);
    setError('');
    setResult(null);
    
    try {
      console.log('Generating meme with:', { situation, style, mood });
      const response = await memeAPI.generateMeme(situation, style, mood);
      console.log('Response:', response.data);
      setResult(response.data);
      setSituation('');
    } catch (err) {
      const errorMsg = err.response?.data?.error || err.message || 'Failed to generate meme';
      setError(errorMsg);
      console.error('Generation error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="generator-container">
      <div className="generator-card">
        <h2>🎨 Create a Meme</h2>
        
        <form onSubmit={handleGenerate} className="form">
          <div className="form-group">
            <label htmlFor="situation">Describe your situation:</label>
            <textarea
              id="situation"
              value={situation}
              onChange={(e) => setSituation(e.target.value)}
              placeholder="e.g., When you fix a bug but create three new ones"
              rows="4"
              disabled={loading}
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="style">Style:</label>
              <select 
                id="style"
                value={style} 
                onChange={(e) => setStyle(e.target.value)}
                disabled={loading}
              >
                <option value="cartoon/animation">Cartoon/Animation</option>
                <option value="realistic">Realistic</option>
                <option value="meme-style">Meme Style</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="mood">Mood:</label>
              <select 
                id="mood"
                value={mood} 
                onChange={(e) => setMood(e.target.value)}
                disabled={loading}
              >
                <option value="funny">Funny</option>
                <option value="sarcastic">Sarcastic</option>
                <option value="dramatic">Dramatic</option>
              </select>
            </div>
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="btn-generate"
          >
            {loading ? '⏳ Generating... (may take a minute)' : '🔥 Generate Meme'}
          </button>
        </form>

        {error && (
          <div className="error-box">
            <p>❌ {error}</p>
          </div>
        )}
        
        {result && (
          <div className="result-box">
            <h3>✅ Your Meme Created!</h3>
            <img 
              src={`http://localhost:5000/${result.image_path.replace(/\\/g, '/')}`}
              alt="Generated meme" 
              className="meme-image"
              onError={(e) => {
                console.error('Image failed to load from:', e.target.src);
                e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="300"%3E%3Crect fill="%23cccccc" width="400" height="300"/%3E%3Ctext x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-family="Arial" font-size="16" fill="%23666666"%3EImage not found%3C/text%3E%3C/svg%3E';
              }}
              onLoad={() => console.log('Image loaded successfully:', result.image_path)}
            />
            <p className="meme-text"><strong>Text:</strong> {result.text}</p>
            <div className="result-actions">
              <a 
                href={`http://localhost:5000/${result.image_path.replace(/\\/g, '/')}`}
                download 
                className="btn-download"
              >
                ⬇️ Download
              </a>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}