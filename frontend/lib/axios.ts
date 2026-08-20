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

const IT_SERVICE_URL = process.env.NEXT_PUBLIC_IT_SERVICE_URL || "http://localhost:8004";
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

const WORKFLOW_SERVICE_URL = process.env.NEXT_PUBLIC_WORKFLOW_SERVICE_URL || "http://localhost:8005";
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

const AI_SERVICE_URL = process.env.NEXT_PUBLIC_AI_SERVICE_URL || "http://localhost:8003";
export const aiApi = axios.create({
  baseURL: AI_SERVICE_URL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

aiApi.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

const ANALYTICS_SERVICE_URL = process.env.NEXT_PUBLIC_ANALYTICS_SERVICE_URL || "http://localhost:8007";
export const analyticsApi = axios.create({
  baseURL: ANALYTICS_SERVICE_URL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

analyticsApi.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// --- Response Interceptor Setup ---
import toast from "react-hot-toast";

const responseInterceptor = (response: any) => response;

const errorInterceptor = async (error: any) => {
  if (error.response) {
    const status = error.response.status;
    
    // Auto-logout on 401 (Unauthorized), unless it's the login, logout, or refresh endpoint
    if (status === 401 && !error.config.url?.includes("/login") && !error.config.url?.includes("/logout") && !error.config.url?.includes("/refresh")) {
      toast.error("Session expired. Please log in again.");
      useAuthStore.getState().logout();
      window.location.href = "/login";
    }
    
    // Toast on 403 (Forbidden)
    if (status === 403) {
      toast.error("You do not have permission to perform this action.");
    }
    
    // Toast on 500+ (Server errors)
    if (status >= 500) {
      toast.error("An unexpected server error occurred. Please try again later.");
    }
  } else if (error.request) {
    // Network errors (no response)
    toast.error("Network error. Please check your connection.");
  }

  return Promise.reject(error);
};

api.interceptors.response.use(responseInterceptor, errorInterceptor);
hrApi.interceptors.response.use(responseInterceptor, errorInterceptor);
itApi.interceptors.response.use(responseInterceptor, errorInterceptor);
workflowApi.interceptors.response.use(responseInterceptor, errorInterceptor);
aiApi.interceptors.response.use(responseInterceptor, errorInterceptor);
analyticsApi.interceptors.response.use(responseInterceptor, errorInterceptor);
