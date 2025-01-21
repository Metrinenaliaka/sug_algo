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
export const signup = async (userData) => {
  const response = await axios.post('http://127.0.0.1:8000/api/signup/', userData);
  return response.data;  // Returning the response message or data from the backend
};
axios.defaults.withCredentials = true;
axios.interceptors.request.use((config) => {
  const token = document.cookie.match(/csrftoken=([^;]+)/)?.[1];  // Get CSRF token from cookie
  if (token) {
    config.headers['X-CSRFToken'] = token;  // Add CSRF token to request headers
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});
// Login an existing user
export const login = async (userData) => {
  const response = await axios.post('http://127.0.0.1:8000/api/login/', userData, {
    withCredentials: true, // Send cookies with the request for session management
  });
  return response.data;  // Returning the response message or data from the backend
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