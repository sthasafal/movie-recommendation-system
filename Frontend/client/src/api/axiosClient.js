import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Real API functions - Uncomment and use these instead of mockAPI
export const realAPI = {
  getRecommended: (userId) => {
    return api.get(`/recommend/${userId}`).then(res => res.data);
  },

  getSimilar: (movieId) => {
    return api.get(`/recommend/similar/${movieId}`).then(res => res.data);
  },

  getTrending: () => {
    return api.get('/trending').then(res => res.data);
  },

  searchMovies: (query) => {
    return api.get(`/search?query=${query}`).then(res => res.data);
  },
};

export default api;