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
          <p class="text-gray-600 font-semibold">{{ comment.author }}</p>
          <p class="text-gray-700">{{ comment.content }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from "vue";
import { useBlogStore, BlogPost } from "@/stores/blogPostStore";
import { useUserStore } from "@/stores/userStore";
import { useRoute } from "vue-router";

export default defineComponent({
  setup() {
    const blogStore = useBlogStore();
    const userStore = useUserStore();
    const route = useRoute();
    const post = ref<BlogPost | null>(null);
    const comments = ref([
      { id: 1, author: "John Doe", content: "Great post!" },
      { id: 2, author: "Jane Smith", content: "Thanks for sharing!" },
      { id: 3, author: "Bob Johnson", content: "Very informative." },
      { id: 4, author: "Alice Walker", content: "I learned a lot!" },
      { id: 5, author: "Michael Brown", content: "Fantastic read!" },
      { id: 6, author: "Emily Davis", content: "Well written!" },
      { id: 7, author: "James Wilson", content: "I agree with you." },
      { id: 8, author: "Linda Taylor", content: "Insightful!" },
      { id: 9, author: "Robert Anderson", content: "Keep it up!" },
      { id: 10, author: "Patricia Thomas", content: "Very helpful!" },
      { id: 11, author: "David Martinez", content: "Excellent article!" },
      {
        id: 12,
        author: "Jennifer Garcia",
        content: "I appreciate your insights.",
      },
      { id: 13, author: "Charles Rodriguez", content: "This was great!" },
      { id: 14, author: "Susan Lee", content: "Love this content!" },
      { id: 15, author: "Joseph Gonzalez", content: "Informative post!" },
      { id: 16, author: "Mary Perez", content: "I enjoyed reading this." },
      { id: 17, author: "Thomas Wilson", content: "So interesting!" },
      { id: 18, author: "Lisa White", content: "Can't wait for more!" },
      { id: 19, author: "Daniel Harris", content: "This is a gem!" },
      { id: 20, author: "Karen Clark", content: "You made my day!" },
    ]);
    const newComment = ref("");

    const deletePost = async (postId: number) => {
      const confirmed = confirm("Are you sure you want to delete this post?");
      if (confirmed) {
        await blogStore.deletePost(postId);
      }
    };

    const loadPost = async () => {
      const postId = Number(route.params.id);
      if (!isNaN(postId)) {
        await blogStore.fetchPost(postId);
        post.value = blogStore.currentPost;
      }
    };

    const canEditOrDelete = computed(() => {
      return userStore.user?.id === post.value?.author.id;
    });

    const addComment = () => {
      if (newComment.value.trim()) {
        comments.value.push({
          id: comments.value.length + 1,
          author: userStore.user?.username || "Anonymous",
          content: newComment.value.trim(),
        });
        newComment.value = ""; // Clear the input after submission
      }
    };

    onMounted(loadPost);

    return {
      post,
      deletePost,
      canEditOrDelete,
      comments,
      newComment,
      addComment,
    };
  },
});
</script>
