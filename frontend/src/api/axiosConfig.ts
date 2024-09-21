import axios from "axios";
import { useUserStore } from "../stores/userStore";

const axiosInstance = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL,
});

//request interceptor to include the access token
axiosInstance.interceptors.request.use(
  (config) => {
    const userStore = useUserStore();
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

//response interceptor for handling token refresh
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const userStore = useUserStore();

    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const response = await axios.post("/api/token/refresh/", {
          refresh: userStore.refreshToken,
        });

        userStore.token = response.data.access;
        if (userStore.token)
          localStorage.setItem("access_token", userStore.token);

        axios.defaults.headers.common.Authorization = `Bearer ${userStore.token}`;

        originalRequest.headers.Authorization = `Bearer ${userStore.token}`;

        return axiosInstance(originalRequest);
      } catch (refreshError) {
        userStore.logout();
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default axiosInstance;
