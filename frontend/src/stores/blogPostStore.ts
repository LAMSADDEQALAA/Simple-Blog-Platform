// src/stores/blogStore.ts
import { defineStore } from "pinia";
import axios from "../api/axiosConfig";
import { handleError } from "../utils/handleError"; // Import your error handling function

export interface BlogPost {
  id: number;
  title: string;
  content: string;
  author: string;
  created_at: string;
  updated_at: string;
}

interface BlogState {
  posts: BlogPost[];
  currentPost: BlogPost | null;
}

export const useBlogStore = defineStore("blog", {
  state: (): BlogState => ({
    posts: [],
    currentPost: null,
  }),
  actions: {
    async fetchPosts(page = 1) {
      try {
        const response = await axios.get(`/api/BlogPosts/?page=${page}`);
        this.posts = response.data;
      } catch (error) {
        handleError(error);
      }
    },
  },
});
