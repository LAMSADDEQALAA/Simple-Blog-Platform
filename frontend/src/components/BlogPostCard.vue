<template>
  <div class="border p-4 rounded-lg shadow-md">
    <h2 class="text-xl font-bold mb-2">{{ post?.title }}</h2>
    <p class="text-gray-600">By {{ post?.author.username }}</p>
    <p class="text-gray-800">{{ post?.content.substring(0, 100) }}...</p>
    <router-link
      :to="`/posts/${post?.id}`"
      class="text-blue-500 hover:underline"
      >Read more</router-link
    >
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    post: Object,
  },
});
</script>
``
