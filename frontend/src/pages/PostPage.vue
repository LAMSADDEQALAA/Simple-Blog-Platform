<template>
  <div class="max-w-3xl mx-auto p-8">
    <h1 class="text-3xl font-bold mb-4">{{ post?.title }}</h1>
    <p class="text-gray-600 mb-6">By {{ post?.author.username }}</p>
    <p class="mb-6">{{ post?.content }}</p>
  </div>
  <div v-if="canEditOrDelete" class="mt-2">
    <router-link
      :to="`/posts/${post?.id}/edit`"
      class="text-white bg-yellow-500 hover:bg-yellow-600 py-1 px-3 rounded mr-4"
    >
      Update
    </router-link>
    <button
      @click="post?.id !== undefined ? deletePost(post.id) : null"
      class="text-white bg-red-500 hover:bg-red-600 py-1 px-3 rounded"
    >
      Delete
    </button>
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

    onMounted(loadPost);

    return {
      post,
      deletePost,
      canEditOrDelete,
    };
  },
});
</script>
