import axios from "axios";
import { useUserStore } from "../stores/userStore";
const createAxiosInstance = (baseURL: string) => {
  const axiosInstance = axios.create({
    baseURL,
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
          const response = await axios.post(
            `${process.env.VUE_APP_CORE_SERVICE_URL}/api/users/token/refresh/`,
            {
              refresh: userStore.refreshToken,
            }
          );

          userStore.token = response.data.access;

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
  return axiosInstance;
};

export const axiosCore = createAxiosInstance(
  process.env.VUE_APP_CORE_SERVICE_URL
);
export const axiosComment = createAxiosInstance(
  process.env.VUE_APP_COMMENT_SERVICE_URL
);
