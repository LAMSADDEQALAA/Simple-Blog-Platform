<template>
  <div class="max-w-4xl mx-auto p-8 bg-white shadow-md rounded-lg mt-12">
    <h1 class="text-3xl font-bold mb-6 text-gray-800">
      {{ isEdit ? "Edit Post" : "Create New Post" }}
    </h1>
    <form @submit.prevent="submitForm" class="space-y-4">
      <div>
        <input
          :value="values.title"
          @input="event => setFieldValue('title', (event.target as HTMLInputElement).value)"
          type="text"
          placeholder="Post Title"
          class="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <span
          v-if="errors.title && isFieldTouched('title')"
          class="text-red-500 text-sm"
        >
          {{ errors.title }}
        </span>
      </div>
      <div>
        <textarea
          :value="values.content"
          @input="event => setFieldValue('content', (event.target as HTMLTextAreaElement).value)"
          placeholder="Post Content"
          class="w-full p-3 border border-gray-300 rounded h-48 focus:outline-none focus:ring-2 focus:ring-blue-500"
        ></textarea>
        <span
          v-if="errors.content && isFieldTouched('title')"
          class="text-red-500 text-sm"
        >
          {{ errors.content }}
        </span>
      </div>
      <button
        type="submit"
        class="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition"
      >
        {{ isEdit ? "Update" : "Create" }} Post
      </button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useBlogStore } from "@/stores/blogPostStore";
import { useRoute, useRouter } from "vue-router";
import { useForm } from "vee-validate";
import * as yup from "yup";

export default defineComponent({
  setup() {
    const blogStore = useBlogStore();
    const route = useRoute();
    const router = useRouter();
    const isEdit = ref(false);

    const schema = yup.object({
      title: yup
        .string()
        .required("Post title is required")
        .min(3, "Title must be at least 3 characters long"),
      content: yup
        .string()
        .required("Content is required")
        .min(10, "Content must be at least 10 characters long"),
    });

    const { values, errors, handleSubmit, setFieldValue, isFieldTouched } =
      useForm({
        validationSchema: schema,
        initialValues: {
          title: "",
          content: "",
        },
      });

    const loadPost = async () => {
      const postId = Number(route.params.id);
      if (!isNaN(postId)) {
        isEdit.value = true;
        await blogStore.fetchPost(postId);
        setFieldValue("title", blogStore.currentPost?.title || "");
        setFieldValue("content", blogStore.currentPost?.content || "");
      }
    };

    const submitForm = handleSubmit(async () => {
      const postId = Number(route.params.id);
      const data = {
        title: values.title,
        content: values.content,
      };
      if (isEdit.value && !isNaN(postId)) {
        await blogStore.updatePost(postId, data);
      } else {
        await blogStore.createPost(data);
      }
      router.back();
    });

    onMounted(loadPost);

    return {
      values,
      errors,
      submitForm,
      isEdit,
      setFieldValue,
      isFieldTouched,
    };
  },
});
</script>
