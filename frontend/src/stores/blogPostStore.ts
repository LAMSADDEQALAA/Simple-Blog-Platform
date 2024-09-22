import { defineStore } from "pinia";
import { axiosCore } from "../api/axiosConfig";
import { handleError } from "@/utils/handleError";
import { notyf } from "../utils/toast";

export interface BlogPost {
  id: number;
  title: string;
  content: string;
  author: { id: number; username: "" };
  created_at: string;
  updated_at: string;
}

interface BlogState {
  posts: BlogPost[];
  currentPost: BlogPost | null;
  totalPages: number;
}

export const useBlogStore = defineStore("blog", {
  state: (): BlogState => ({
    posts: [],
    currentPost: null,
    totalPages: 1,
  }),
  actions: {
    async fetchPosts(query = "", page = 1) {
      try {
        const response = await axiosCore.get(
          `/api/BlogPosts/?search=${query}&page=${page}`
        );
        this.posts = response.data.results;
        this.totalPages = Math.ceil(response.data.count / 15);
      } catch (error) {
        handleError(error);
      }
    },
    async fetchPost(postId: number) {
      try {
        const response = await axiosCore.get(`/api/BlogPosts/${postId}/`);
        this.currentPost = response.data;
      } catch (error) {
        handleError(error);
      }
    },
    async createPost(postData: { title: string; content: string }) {
      try {
        await axiosCore.post("/api/BlogPosts/", postData);
        await this.fetchPosts();
        notyf.success("BlogPost created successfuly!");
      } catch (error) {
        handleError(error);
      }
    },
    async updatePost(
      postId: number,
      postData: { title: string; content: string }
    ) {
      try {
        await axiosCore.put(`/api/BlogPosts/${postId}/`, postData);
        await this.fetchPosts();
        notyf.success("BlogPost updated successfuly!");
      } catch (error) {
        handleError(error);
      }
    },
    async deletePost(postId: number) {
      try {
        await axiosCore.delete(`/api/BlogPosts/${postId}/`);
        await this.fetchPosts();
        notyf.success("BlogPost deleted successfuly!");
      } catch (error) {
        handleError(error);
      }
    },
  },
});
