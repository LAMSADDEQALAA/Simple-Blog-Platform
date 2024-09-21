<template>
  <div class="container mx-auto">
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      <BlogPostCard v-for="post in posts" :key="post.id" :post="post" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from "vue";
import { useBlogStore } from "../stores/blogPostStore";
import BlogPostCard from "@/components/BlogPostCard.vue";

export default defineComponent({
  components: { BlogPostCard },
  setup() {
    const blogStore = useBlogStore();
    const posts = ref(blogStore.posts);
    const searchQuery = ref("");
    const currentPage = ref(1);

    const loadPosts = async () => {
      await blogStore.fetchPosts(currentPage.value);
      posts.value = blogStore.posts;
    };

    const changePage = async (page: number) => {
      currentPage.value = page;
      await loadPosts();
    };

    onMounted(loadPosts);

    watch(
      () => blogStore.posts,
      (newPosts) => {
        posts.value = newPosts;
      }
    );

    return {
      posts,
      searchQuery,
      currentPage,
      changePage,
    };
  },
});
</script>

<style scoped>
.container {
  padding: 2rem;
}
</style>
