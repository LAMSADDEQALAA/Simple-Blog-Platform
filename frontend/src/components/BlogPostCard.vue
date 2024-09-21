<template>
  <div class="border p-4 rounded-lg shadow-md hover:shadow-lg transition">
    <h2 class="text-xl font-bold mb-2">{{ post?.title }}</h2>
    <p class="text-gray-600">By {{ post?.author.username }}</p>
    <p class="text-gray-800">{{ post?.content.substring(0, 100) }}...</p>
    <router-link
      :to="`/posts/${post?.id}`"
      class="text-blue-500 hover:underline"
    >
      Read more
    </router-link>
    <div v-if="canEditOrDelete" class="mt-2">
      <router-link
        :to="`/posts/${post?.id}/edit`"
        class="text-white bg-yellow-500 hover:bg-yellow-600 py-1 px-3 rounded mr-4"
      >
        Update
      </router-link>
      <button
        @click="deletePost(post?.id)"
        class="text-white bg-red-500 hover:bg-red-600 py-1 px-3 rounded"
      >
        Delete
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import { useUserStore } from "@/stores/userStore";
import { useBlogStore } from "@/stores/blogPostStore";

export default defineComponent({
  props: {
    post: Object,
  },
  setup(props) {
    const userStore = useUserStore();
    const blogStore = useBlogStore();

    const canEditOrDelete = computed(() => {
      return userStore.user?.id === props.post?.author.id;
    });

    const deletePost = async (postId: number) => {
      const confirmed = confirm("Are you sure you want to delete this post?");
      if (confirmed) {
        await blogStore.deletePost(postId);
      }
    };

    return {
      canEditOrDelete,
      deletePost,
    };
  },
});
</script>
