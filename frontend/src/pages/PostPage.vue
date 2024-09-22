<template>
  <div class="max-w-4xl mx-auto p-8 bg-white shadow-md rounded-lg mt-12">
    <h1 class="text-4xl font-bold mb-4 text-gray-800">{{ post?.title }}</h1>
    <p class="text-gray-600 mb-6">
      By <span class="font-semibold">{{ post?.author.username }}</span>
    </p>
    <p class="text-gray-700 mb-6 text-lg leading-relaxed">
      {{ post?.content }}
    </p>

    <div v-if="canEditOrDelete" class="flex mt-4 space-x-4">
      <router-link
        :to="`/posts/${post?.id}/edit`"
        class="text-white bg-yellow-500 hover:bg-yellow-600 py-2 px-4 rounded-lg shadow transition"
      >
        Update
      </router-link>
      <button
        @click="post?.id !== undefined ? deletePost(post.id) : null"
        class="text-white bg-red-500 hover:bg-red-600 py-2 px-4 rounded-lg shadow transition"
      >
        Delete
      </button>
    </div>

    <h2 class="text-3xl font-bold mt-8 mb-4 text-gray-800">Comments</h2>
    <div class="border-t border-gray-300 pt-4">
      <div class="mt-4 mb-4">
        <input
          v-model="newComment"
          type="text"
          placeholder="Add a comment..."
          class="border border-gray-300 rounded-lg p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          @click="addComment"
          class="mt-2 text-white bg-blue-500 hover:bg-blue-600 py-2 px-4 rounded-lg shadow transition"
        >
          Submit
        </button>
      </div>

      <div class="max-h-60 overflow-y-auto" style="max-height: 300px">
        <div
          v-for="comment in comments"
          :key="comment.id"
          class="mb-4 p-4 border border-gray-200 rounded-lg"
        >
          <p class="text-gray-600 font-semibold">{{ comment.user_id }}</p>
          <p class="text-gray-700">{{ comment.content }}</p>
          <button
            v-if="canDeleteComment(comment)"
            @click="deleteComment(comment.id)"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from "vue";
import { useBlogStore, BlogPost } from "@/stores/blogPostStore";
import { useUserStore } from "@/stores/userStore";
import { useCommentStore, Comment } from "@/stores/commentStore";
import { useRoute } from "vue-router";

export default defineComponent({
  setup() {
    const blogStore = useBlogStore();
    const userStore = useUserStore();
    const commentStore = useCommentStore();

    const route = useRoute();
    const post = ref<BlogPost | null>(null);
    const comments = ref<Comment[] | null>(null);
    const newComment = ref("");
    const postId = Number(route.params.id);

    const deletePost = async (postId: number) => {
      const confirmed = confirm("Are you sure you want to delete this post?");
      if (confirmed) {
        await blogStore.deletePost(postId);
      }
    };

    const loadPost = async () => {
      if (!isNaN(postId)) {
        await blogStore.fetchPost(postId);
        post.value = blogStore.currentPost;
      }
    };

    const canEditOrDelete = computed(() => {
      return userStore.user?.id === post.value?.author.id;
    });

    const addComment = () => {
      const content = newComment.value.trim();
      if (content && postId) {
        commentStore.addComment(postId, content);
        newComment.value = "";
      }
    };

    const deleteComment = (commentId: number) => {
      commentStore.deleteComment(postId, commentId);
    };

    const canDeleteComment = (user_id: number) => {
      return userStore.user?.id === user_id || userStore.user?.id === user_id;
    };

    onMounted(async () => {
      await loadPost();
      await commentStore.fetchComments(postId);
      comments.value = commentStore.comments;
    });

    return {
      post,
      deletePost,
      canEditOrDelete,
      comments,
      newComment,
      addComment,
      deleteComment,
      canDeleteComment,
    };
  },
});
</script>
