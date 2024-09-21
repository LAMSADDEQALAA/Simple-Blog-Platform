import { defineStore } from "pinia";
import axios from "../api/axiosConfig";

interface User {
  id: number;
  username: string;
}

interface UserState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
}

export const useUserStore = defineStore("user", {
  state: (): UserState => ({
    user: null,
    token: localStorage.getItem("access_token") || null,
    refreshToken: localStorage.getItem("refresh_token") || null,
  }),
  actions: {
    async register(userData: { username: string; password: string }) {
      const response = await axios.post("/api/users/register/", userData);
      this.user = response.data;
    },
    async login(credentials: { username: string; password: string }) {
      const response = await axios.post("/api/token/", credentials);
      this.token = response.data.access;
      this.refreshToken = response.data.refresh;

      if (!this.token || !this.refreshToken) {
        throw new Error("Failed to authenticate");
      }

      localStorage.setItem("access_token", this.token);
      localStorage.setItem("refresh_token", this.refreshToken);
    },
    logout() {
      this.user = null;
      this.token = null;
      this.refreshToken = null;

      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    },
  },
});
