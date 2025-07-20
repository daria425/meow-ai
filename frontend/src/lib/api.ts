import axios from "axios";

const isDevelopment = process.env.NODE_ENV === "development";

const api = axios.create({
  baseURL: isDevelopment
    ? "http://127.0.0.1:5000"
    : process.env.VITE_PUBLIC_API_URL || "https://my-production-api.com",
});

export default api;
