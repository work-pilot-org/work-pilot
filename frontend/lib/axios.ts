import axios from "axios";
import { useAuthStore } from "@/store/authStore";

const AUTH_SERVICE_URL = process.env.NEXT_PUBLIC_AUTH_SERVICE_URL || "http://localhost:8001";
const HR_SERVICE_URL = process.env.NEXT_PUBLIC_HR_SERVICE_URL || "http://localhost:8002";

export const api = axios.create({
  baseURL: AUTH_SERVICE_URL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const hrApi = axios.create({
  baseURL: HR_SERVICE_URL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

hrApi.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

const IT_SERVICE_URL = process.env.NEXT_PUBLIC_IT_SERVICE_URL || "http://localhost:8003";
export const itApi = axios.create({
  baseURL: IT_SERVICE_URL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

itApi.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

const WORKFLOW_SERVICE_URL = process.env.NEXT_PUBLIC_WORKFLOW_SERVICE_URL || "http://localhost:8004";
export const workflowApi = axios.create({
  baseURL: WORKFLOW_SERVICE_URL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

workflowApi.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

