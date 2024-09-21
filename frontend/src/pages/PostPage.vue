<template>
  <div class="max-w-3xl mx-auto p-8">
    <h1 class="text-3xl font-bold mb-4">{{ post?.title }}</h1>
    <p class="text-gray-600 mb-6">By {{ post?.author.username }}</p>
    <p class="mb-6">{{ post?.content }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useBlogStore, BlogPost } from "@/stores/blogPostStore";
import { useRoute } from "vue-router";

export default defineComponent({
  setup() {
    const blogStore = useBlogStore();
    const route = useRoute();
    const post = ref<BlogPost | null>(null);

    const loadPost = async () => {
      const postId = Number(route.params.id);
      if (!isNaN(postId)) {
        await blogStore.fetchPost(postId);
        post.value = blogStore.currentPost;
      }
    };

    onMounted(loadPost);

    return {
      post,
    };
  },
});
</script>
