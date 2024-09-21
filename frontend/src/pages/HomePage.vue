<template>
  <div class="container mx-auto">
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      <BlogPostCard v-for="post in posts" :key="post.id" :post="post" />
    </div>
    <BlogPagination
      :totalPages="totalPages"
      :currentPage="currentPage"
      @pageChange="changePage"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useBlogStore } from "../stores/blogPostStore";
import BlogPostCard from "../components/BlogPostCard.vue";
import BlogPagination from "../components/BlogPagination.vue";

export default defineComponent({
  components: { BlogPostCard, BlogPagination },
  setup() {
    const blogStore = useBlogStore();
    const posts = ref(blogStore.posts);
    const currentPage = ref(1);
    const totalPages = ref(1);

    const loadPosts = async () => {
      await blogStore.fetchPosts("", currentPage.value);
      posts.value = blogStore.posts;
      totalPages.value = blogStore.totalPages;
    };

    const changePage = async (page: number) => {
      currentPage.value = page;
      await loadPosts();
    };

    onMounted(loadPosts);

    return {
      posts,
      currentPage,
      totalPages,
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
