import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

export const memeAPI = {
  generateMeme: (situation, style, mood) =>
    axios.post(`${API_BASE}/generate`, { situation, style, mood }),
  
  batchGenerate: (situations) =>
    axios.post(`${API_BASE}/batch`, { situations }),
  
  listMemes: () =>
    axios.get(`${API_BASE}/memes`),
  
  deleteMeme: (filename) =>
    axios.delete(`${API_BASE}/memes/${filename}`),
  
  health: () =>
    axios.get(`${API_BASE}/health`)
};