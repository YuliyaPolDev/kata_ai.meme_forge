import React, { useState, useEffect } from 'react';
import { memeAPI } from './services/api';
import MemeGenerator from './components/MemeGenerator';
import MemeGallery from './components/MemeGallery';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('generator');
  const [isConnected, setIsConnected] = useState(false);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    // Check backend connection on mount
    checkBackendConnection();
  }, []);

  const checkBackendConnection = async () => {
    try {
      await memeAPI.health();
      setIsConnected(true);
    } catch (err) {
      setIsConnected(false);
      console.error('Backend connection failed:', err);
    } finally {
      setChecking(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>🔥 Meme Forge</h1>
          <p className="subtitle">AI-powered workplace meme generator</p>
        </div>
        <div className="connection-status">
          {checking ? (
            <span className="status checking">🔄 Checking...</span>
          ) : isConnected ? (
            <span className="status connected">✅ Connected</span>
          ) : (
            <span className="status disconnected">
              ❌ Backend offline (running on http://localhost:5000?)
            </span>
          )}
        </div>
      </header>

      <nav className="app-nav">
        <button 
          onClick={() => setActiveTab('generator')}
          className={`nav-btn ${activeTab === 'generator' ? 'active' : ''}`}
        >
          🎨 Create
        </button>
        <button 
          onClick={() => setActiveTab('gallery')}
          className={`nav-btn ${activeTab === 'gallery' ? 'active' : ''}`}
        >
          📸 Gallery
        </button>
      </nav>

      <main className="app-main">
        {!isConnected && !checking && (
          <div className="warning-box">
            <h3>⚠️ Backend Not Connected</h3>
            <p>Make sure Flask server is running on http://localhost:5000</p>
            <button onClick={checkBackendConnection}>Retry Connection</button>
          </div>
        )}
        
        {activeTab === 'generator' && <MemeGenerator />}
        {activeTab === 'gallery' && <MemeGallery />}
      </main>

      <footer className="app-footer">
        <p>© 2025 Meme Forge | Powered by AI</p>
      </footer>
    </div>
  );
}

export default App;