<template>
  <div class="mb-4 p-4 border border-gray-200 rounded-lg relative">
    <form v-if="isEditing" @submit.prevent="submitEditComment">
      <div>
        <input
          :value="values.editedComment"
          @input="event => setFieldValue('editedComment', (event.target as HTMLInputElement).value)"
          type="text"
          placeholder="Edit your comment..."
          class="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <p v-if="errors.editedComment" class="text-red-500">
          {{ errors.editedComment }}
        </p>
        <button
          type="submit"
          class="text-white bg-green-500 hover:bg-green-600 py-2 px-4 rounded-lg shadow transition mt-2"
        >
          Update
        </button>
        <button
          @click="cancelEdit"
          class="text-white bg-gray-500 hover:bg-gray-600 py-2 px-4 rounded-lg shadow transition ml-2 mt-2"
        >
          Cancel
        </button>
      </div>
    </form>

    <div v-else>
      <p class="text-gray-600 font-semibold">{{ comment.username }}</p>
      <p class="text-gray-700">{{ comment.content }}</p>
    </div>

    <div v-if="canEditOrDelete" class="absolute top-0 right-0 me-2">
      <button
        @click="isEditing = true"
        class="text-blue-500 hover:text-blue-600"
      >
        Edit
      </button>
      <button
        @click="deleteComment"
        class="text-red-500 hover:text-red-600 ml-2"
      >
        X
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from "vue";
import { useCommentStore, Comment as CommentType } from "@/stores/commentStore";
import { useUserStore } from "@/stores/userStore";
import * as yup from "yup";
import { useForm } from "vee-validate";

export default defineComponent({
  props: {
    comment: { type: Object as () => CommentType, required: true },
    postId: { type: Number, required: true },
  },
  setup(props) {
    const userStore = useUserStore();
    const commentStore = useCommentStore();

    const isEditing = ref(false);

    const schema = yup.object({
      editedComment: yup
        .string()
        .required("Comment is required")
        .min(3, "Comment must be at least 3 characters"),
    });

    const { handleSubmit, errors, values, setFieldValue } = useForm({
      validationSchema: schema,
      initialValues: {
        editedComment: props.comment.content,
      },
    });

    const canEditOrDelete = computed(
      () => userStore.user?.id === props.comment.user_id
    );

    const deleteComment = async () => {
      const confirmed = confirm(
        "Are you sure you want to delete this comment?"
      );
      if (confirmed) {
        await commentStore.deleteComment(props.postId, props.comment.id);
        await commentStore.fetchComments(props.postId);
      }
    };

    const submitEditComment = handleSubmit(async () => {
      const editedContent = values.editedComment.trim();
      await commentStore.updateComment(
        props.postId,
        props.comment.id,
        editedContent
      );
      isEditing.value = false;
      await commentStore.fetchComments(props.postId);
    });

    const cancelEdit = () => {
      isEditing.value = false;
      setFieldValue("editedComment", props.comment.content);
    };

    return {
      isEditing,
      values,
      errors,
      setFieldValue,
      canEditOrDelete,
      deleteComment,
      submitEditComment,
      cancelEdit,
    };
  },
});
</script>
