import { defineStore } from "pinia";
import axios from "axios";

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
    token: "" || null,
    refreshToken: "" || null,
  }),
  actions: {},
});
