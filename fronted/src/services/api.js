import axios from "axios";

const API_BASE = `${import.meta.env.VITE_API_URL}/api`;

// Devuelve la lista de archivos CSV sin extensión
export const obtenerArchivos = () => axios.get(`${API_BASE}/archivos/`);

// Ejecuta un requerimiento específico para un archivo
export const ejecutarRequerimiento = (nombreRequerimiento, archivo) =>
  axios.get(`${API_BASE}/${nombreRequerimiento}/?archivo=${archivo}`);
