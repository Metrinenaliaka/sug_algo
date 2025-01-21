import axios from 'axios';

const API_URL = 'http://localhost:8000/api';  // Change this to your backend URL

// Helper to get the JWT token from localStorage
const getToken = () => localStorage.getItem('token');

// Create Axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add Authorization header with token for authenticated routes
api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});

// Sign up a new user
export const signup = async (data) => {
  const response = await api.post('/signup/', data);
  return response.data;
};

// Login an existing user
export const login = async (data) => {
  const response = await api.post('/login/', data);
  return response.data;
};

// Fetch user profile (including preferences)
export const getUserProfile = async () => {
  const response = await api.get('/user_profile/');
  return response.data;
};

// Fetch recommended products based on user preferences
export const getProductRecommendations = async () => {
  const response = await api.get('/product_recommendations/');
  return response.data;
};

export default api;