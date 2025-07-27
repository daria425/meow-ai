import axios from "axios";

const isDevelopment = import.meta.env.MODE === "development";
let websocketUrl = `ws://127.0.0.1:8000/ws/cartoonize-cat/`;
const publicAPIUrl = import.meta.env.VITE_PUBLIC_API_URL;
if (import.meta.env.MODE === "production" && publicAPIUrl) {
  websocketUrl = `wss://${publicAPIUrl.replace(
    "https://",
    ""
  )}/ws/cartoonize-cat/`;
}
const api = axios.create({
  baseURL: isDevelopment ? "http://127.0.0.1:8000" : publicAPIUrl,
});

export { api, websocketUrl };
