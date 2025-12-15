import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    withCredentials: true,
});

let isRefreshing = false;

api.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;

        if (error.response?.status !== 401) {
            return Promise.reject(error);
        }

        if (originalRequest._retry) {
            window.location.href = "/login/";
            return Promise.reject(error);
        }

        originalRequest._retry = true;

        if (isRefreshing) {
            return Promise.reject(error);
        }

        isRefreshing = true;

        try {
            await api.post("/api/token/refresh/");
            isRefreshing = false;

            return api(originalRequest);

        } catch (refreshError) {
            isRefreshing = false;
            window.location.href = "/login/";
            return Promise.reject(refreshError);
        }
    }
);

export default api;
