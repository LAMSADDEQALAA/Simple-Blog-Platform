import { defineStore } from "pinia";
import { axiosComment, axiosCore } from "../api/axiosConfig";
import { handleError } from "../utils/handleError";
import { notyf } from "../utils/toast";
import { User } from "../stores/userStore";
export interface Comment {
  id: number;
  post_id: number;
  user_id: number;
  content: string;
  username?: string;
}

interface CommentState {
  comments: Comment[];
  totalPages: number;
  users: User[];
}

export const useCommentStore = defineStore("comment", {
  state: (): CommentState => ({
    comments: [],
    totalPages: 1,
    users: [],
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
    async addComment(data: {
      user_id: number;
      content: string;
      post_id: number;
    }) {
      try {
        await axiosComment.post(`/api/comments`, data);
        await this.fetchComments(data.post_id);
        notyf.success("Comment added successfully!");
      } catch (error) {
        handleError(error);
      }
    },
    async updateComment(postId: number, commentId: number, content: string) {
      try {
        await axiosComment.put(`/api/comments/${commentId}`, { content });
        await this.fetchComments(postId);
        notyf.success("Comment updated successfully!");
      } catch (error) {
        handleError(error);
      }
    },
    async deleteComment(postId: number, commentId: number) {
      try {
        await axiosComment.delete(`/api/comments/${commentId}`);
        await this.fetchComments(postId); // Refresh the comments list after deleting
        notyf.success("Comment deleted successfully!");
      } catch (error) {
        handleError(error);
      }
    },
    async fetchUsersByIds(userIds: number[]) {
      try {
        const response = await axiosCore.get("/api/users/", {
          params: { ids: userIds.join(",") },
        });
        this.users = response.data;
      } catch (error) {
        handleError(error);
      }
    },
    async getCommentsWithUsernames(comments: Comment[]) {
      const userIds = comments.map((comment) => comment.user_id);
      await this.fetchUsersByIds(userIds);
      return comments.map((comment) => {
        const user = this.users.find((user) => user.id === comment.user_id);
        return {
          ...comment,
          username: user ? user.username : "Unknown",
        };
      });
    },
  },
});
