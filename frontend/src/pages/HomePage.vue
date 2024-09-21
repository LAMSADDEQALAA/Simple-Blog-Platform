<template>
  <div class="container mx-auto p-6">
    <router-link
      to="/posts/create"
      class="mb-6 inline-block bg-green-500 text-white py-2 px-4 rounded shadow-md hover:bg-green-600 transition"
    >
      Create New Post
    </router-link>
    <BlogPostSearchBar :searchQuery="searchQuery" @search="searchPosts" />
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 mt-4">
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
import BlogPostSearchBar from "@/components/BlogPostSearchBar.vue";

export default defineComponent({
  components: { BlogPostCard, BlogPagination, BlogPostSearchBar },
  setup() {
    const blogStore = useBlogStore();
    const posts = ref(blogStore.posts);
    const currentPage = ref(1);
    const totalPages = ref(1);
    const searchQuery = ref("");

    const loadPosts = async () => {
      await blogStore.fetchPosts(searchQuery.value, currentPage.value);
      posts.value = blogStore.posts;
      totalPages.value = blogStore.totalPages;
    };

    const changePage = async (page: number) => {
      currentPage.value = page;
      await loadPosts();
    };

    const searchPosts = async (query: string) => {
      searchQuery.value = query;
      currentPage.value = 1;
      await loadPosts();
    };

    onMounted(loadPosts);

    return {
      posts,
      searchQuery,
      currentPage,
      totalPages,
      changePage,
      searchPosts,
    };
  },
});
</script>
