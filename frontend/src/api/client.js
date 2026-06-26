import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

export const fetchFeatures = () => API.get("/features");
export const predictDisease = (symptoms) => API.post("/predict", { symptoms });

export default API;
