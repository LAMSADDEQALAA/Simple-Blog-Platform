<template>
  <div>
    <form @submit.prevent="submitAddComment">
      <div class="mb-4">
        <input
          :value="values.newComment"
          @input="event => setFieldValue('newComment', (event.target as HTMLInputElement).value)"
          type="text"
          placeholder="Write a comment..."
          class="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <p
          v-if="errors.newComment && isFieldTouched('newComment')"
          class="text-red-500"
        >
          {{ errors.newComment }}
        </p>
      </div>
      <button
        type="submit"
        class="text-white bg-blue-500 hover:bg-blue-600 py-2 px-4 rounded-lg shadow transition"
      >
        Post Comment
      </button>
    </form>

    <div v-if="comments && comments.length > 0" class="pt-2">
      <CommentComp
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        :post-id="postId"
      />
    </div>
    <p v-else class="text-gray-500 mt-4">No comments yet.</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from "vue";
import { useCommentStore, Comment as CommentType } from "@/stores/commentStore";
import CommentComp from "@/components/CommentComp.vue";
import * as yup from "yup";
import { useForm } from "vee-validate";
import { useUserStore } from "@/stores/userStore";

export default defineComponent({
  components: { CommentComp },
  props: {
    postId: { type: Number, required: true },
  },
  setup(props) {
    const commentStore = useCommentStore();
    const comments = ref<CommentType[] | null>(null);
    const userStore = useUserStore();

    const schema = yup.object({
      newComment: yup
        .string()
        .required("Comment is required")
        .min(3, "Comment must be at least 3 characters"),
    });

    const { handleSubmit, errors, values, setFieldValue, isFieldTouched } =
      useForm({
        validationSchema: schema,
        initialValues: {
          newComment: "",
        },
      });

    const loadComments = async () => {
      await commentStore.fetchComments(props.postId);
      comments.value = await commentStore.getCommentsWithUsernames(
        commentStore.comments
      );
    };

    const submitAddComment = handleSubmit(async () => {
      const content = values.newComment.trim();
      const user_id = userStore.user?.id;
      if (content && !isNaN(props.postId) && user_id) {
        await commentStore.addComment({
          user_id,
          content,
          post_id: props.postId,
        });
      }
    });

    watch(
      () => commentStore.comments,
      async (newComments) => {
        comments.value = await commentStore.getCommentsWithUsernames(
          newComments
        );
      }
    );

    onMounted(async () => {
      await loadComments();
    });

    return {
      comments,
      values,
      errors,
      setFieldValue,
      submitAddComment,
      isFieldTouched,
    };
  },
});
</script>
