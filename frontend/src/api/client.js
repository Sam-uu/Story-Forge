import axios from "axios";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE || "http://127.0.0.1:8000",
});

export const generateAll = async (requirement) => {
  const { data } = await api.post("/generate_all", { requirement });
  return data;
};

export const saveCard = async (card) => {
  const { data } = await api.post("/cards", card);
  return data;
};

export const getCards = async () => {
  const { data } = await api.get("/cards");
  return data;
};

export const deleteCard = async (id) => {
  const { data } = await api.delete(`/cards/${id}`);
  return data;
};

export default api;
