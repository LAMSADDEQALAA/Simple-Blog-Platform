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
    <div v-if="post">
      <comment-section :post-id="post.id" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, onMounted, ref } from "vue";
import { useBlogStore, BlogPost } from "@/stores/blogPostStore";
import { useUserStore } from "@/stores/userStore";
import { useRoute } from "vue-router";
import CommentSection from "@/components/CommentSection.vue";

export default defineComponent({
  components: { CommentSection },
  setup() {
    const blogStore = useBlogStore();
    const userStore = useUserStore();

    const route = useRoute();
    const post = ref<BlogPost | null>(null);
    const postId = Number(route.params.id);

    const canEditOrDelete = computed(
      () => userStore.user?.id === post.value?.author.id
    );

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

    onMounted(async () => {
      await loadPost();
    });

    return {
      post,
      canEditOrDelete,
      deletePost,
    };
  },
});
</script>
