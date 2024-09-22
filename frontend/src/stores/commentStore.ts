import { defineStore } from "pinia";
import { axiosComment } from "../api/axiosConfig";
import { handleError } from "../utils/handleError";
import { notyf } from "../utils/toast";

export interface Comment {
  id: number;
  post_id: number;
  user_id: number;
  content: string;
}

interface CommentState {
  comments: Comment[];
  totalPages: number;
}

export const useCommentStore = defineStore("comment", {
  state: (): CommentState => ({
    comments: [],
    totalPages: 1,
  }),
  actions: {
    async fetchComments(postId: number) {
      try {
        const response = await axiosComment.get(
          `/api/posts/${postId}/comments`
        );
        this.comments = response.data;
      } catch (error) {
        handleError(error);
      }
    },
    async addComment(postId: number, content: string) {
      try {
        await axiosComment.post(`/api/posts/${postId}/comments`, { content });
        await this.fetchComments(postId);
        notyf.success("Comment added successfully!");
      } catch (error) {
        handleError(error);
      }
    },
    async deleteComment(postId: number, commentId: number) {
      try {
        await axiosComment.delete(`/api/posts/${postId}/comments/${commentId}`);
        await this.fetchComments(postId); // Refresh the comments list after deleting
        notyf.success("Comment deleted successfully!");
      } catch (error) {
        handleError(error);
      }
    },
  },
});
