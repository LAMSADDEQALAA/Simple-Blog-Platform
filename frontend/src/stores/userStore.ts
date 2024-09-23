import { defineStore } from "pinia";
import { axiosCore } from "../api/axiosConfig";
import { handleError } from "@/utils/handleError";
import { notyf } from "../utils/toast";

export interface User {
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
    user: localStorage.getItem("user")
      ? JSON.parse(localStorage.getItem("user") as string)
      : null,
    token: null,
    refreshToken: localStorage.getItem("refresh_token") || null,
  }),
  actions: {
    async register(userData: { username: string; password: string }) {
      try {
        const response = await axiosCore.post("/api/users/register/", userData);
        this.user = response.data;
        notyf.success("registered successfuly!");
      } catch (error) {
        handleError(error);
      }
    },
    async login(userData: { username: string; password: string }) {
      try {
        const response = await axiosCore.post("/api/users/token/", userData);
        this.token = response.data.access;
        this.refreshToken = response.data.refresh;

        if (!this.token || !this.refreshToken) {
          throw new Error("Failed to authenticate");
        }
        localStorage.setItem("refresh_token", this.refreshToken);

        await this.getUserData();

        notyf.success("loged in successfuly!");
      } catch (error) {
        handleError(error);
      }
    },
    async getUserData() {
      try {
        const response = await axiosCore.get("/api/users/profile/");
        this.user = response.data;
        if (this.user != null) {
          localStorage.setItem("user", JSON.stringify(this.user));
        }
      } catch (error) {
        handleError(error);
      }
    },
    logout() {
      this.user = null;
      this.token = null;
      this.refreshToken = null;

      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("user");
    },
  },
});
