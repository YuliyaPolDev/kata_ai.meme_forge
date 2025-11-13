import React, { useState, useEffect } from 'react';
import { memeAPI } from '../services/api';
import './MemeGallery.css';

export default function MemeGallery() {
  const [memes, setMemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadMemes();
  }, []);

  const loadMemes = async () => {
    try {
      setLoading(true);
      setError('');
      console.log('Loading memes from API...');
      
      const response = await memeAPI.listMemes();
      console.log('API Response:', response.data);
      
      if (response.data.memes && Array.isArray(response.data.memes)) {
        setMemes(response.data.memes);
        console.log(`Loaded ${response.data.memes.length} memes`);
      } else {
        setMemes([]);
      }
    } catch (err) {
      setError('Failed to load memes');
      console.error('Load memes error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (filename) => {
    if (window.confirm('Delete this meme?')) {
      try {
        await memeAPI.deleteMeme(filename);
        setMemes(memes.filter(m => m.filename !== filename));
      } catch (err) {
        setError('Failed to delete meme');
        console.error('Delete error:', err);
      }
    }
  };

  if (loading) {
    return (
      <div className="gallery-container">
        <div className="loading">Loading your memes...</div>
      </div>
    );
  }

  return (
    <div className="gallery-container">
      <div className="gallery-header">
        <h2>📸 Meme Gallery</h2>
        <button onClick={loadMemes} className="btn-refresh">🔄 Refresh</button>
      </div>

      {error && <div className="error-box">{error}</div>}

      {memes.length === 0 ? (
        <div className="empty-gallery">
          <p>No memes yet! Create one to get started 🎨</p>
        </div>
      ) : (
        <div className="meme-grid">
          {memes.map((meme) => (
            <div key={meme.filename} className="meme-card">
              <div className="meme-image-container">
                <img 
                  src={`http://localhost:5000${meme.url}`}
                  alt={meme.filename}
                  className="meme-image"
                  onError={(e) => {
                    console.error(`Failed to load image: ${meme.url}`);
                    e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="250" height="250"%3E%3Crect fill="%23cccccc" width="250" height="250"/%3E%3Ctext x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-family="Arial" font-size="16" fill="%23666666"%3EImage not found%3C/text%3E%3C/svg%3E';
                  }}
                  onLoad={() => console.log(`Loaded image: ${meme.filename}`)}
                />
              </div>
              <div className="card-info">
                <p className="filename">{meme.filename}</p>
              </div>
              <div className="card-actions">
                <a 
                  href={`http://localhost:5000${meme.url}`}
                  download 
                  className="btn-download"
                  title="Download"
                >
                  ⬇️
                </a>
                <button 
                  onClick={() => handleDelete(meme.filename)}
                  className="btn-delete"
                  title="Delete"
                >
                  🗑️
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}