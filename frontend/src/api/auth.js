import axios from "axios";

const BASE_URL = import.meta?.env?.VITE_API_URL || "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: BASE_URL,
});

// Attach Authorization header if token is present in localStorage
api.interceptors.request.use((config) => {
  try {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers = config.headers || {};
      config.headers["Authorization"] = `Bearer ${token}`;
    }
  } catch (err) {
    // ignore (e.g., when localStorage isn't available)
  }
  return config;
});

export default api;
