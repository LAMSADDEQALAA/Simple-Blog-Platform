import { defineStore } from "pinia";

interface BlogPost {
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
  actions: {},
});
