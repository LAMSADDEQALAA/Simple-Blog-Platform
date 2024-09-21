<template>
  <div class="max-w-4xl mx-auto p-8">
    <h1 class="text-2xl font-bold mb-6">
      {{ isEdit ? "Edit Post" : "Create New Post" }}
    </h1>
    <form @submit.prevent="submitPost" class="space-y-4">
      <input
        v-model="title"
        type="text"
        placeholder="Post Title"
        class="w-full p-2 border border-gray-300 rounded"
      />
      <textarea
        v-model="content"
        placeholder="Post Content"
        class="w-full p-2 border border-gray-300 rounded h-48"
      ></textarea>
      <button type="submit" class="bg-blue-500 text-white py-2 px-4 rounded">
        {{ isEdit ? "Update" : "Create" }} Post
      </button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useBlogStore } from "@/stores/blogPostStore";
import { useRoute, useRouter } from "vue-router";

export default defineComponent({
  setup() {
    const blogStore = useBlogStore();
    const route = useRoute();
    const router = useRouter();

    const title = ref<string>("");
    const content = ref<string>("");
    const isEdit = ref(false);

    const loadPost = async () => {
      const postId = Number(route.params.id);
      if (!isNaN(postId)) {
        isEdit.value = true;
        await blogStore.fetchPost(postId);
        title.value = blogStore.currentPost?.title || "";
        content.value = blogStore.currentPost?.content || "";
      }
    };

    const submitPost = async () => {
      const postId = Number(route.params.id);
      const data = {
        title: title.value,
        content: content.value,
      };
      if (isEdit.value && !isNaN(postId)) {
        await blogStore.updatePost(postId, data);
      } else {
        await blogStore.createPost(data);
      }
      router.back();
    };

    onMounted(loadPost);

    return {
      title,
      content,
      isEdit,
      submitPost,
    };
  },
});
</script>
