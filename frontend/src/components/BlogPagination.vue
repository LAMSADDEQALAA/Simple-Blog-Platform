<template>
  <div class="flex justify-center mt-6">
    <button
      @click="prevPage"
      :disabled="currentPage === 1"
      class="px-4 py-2 mx-2 bg-gray-300 rounded disabled:bg-gray-200"
    >
      Prev
    </button>
    <span class="px-4 py-2">{{ currentPage }}</span>
    <button
      @click="nextPage"
      :disabled="currentPage === totalPages"
      class="px-4 py-2 mx-2 bg-gray-300 rounded disabled:bg-gray-200"
    >
      Next
    </button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useRouter } from "vue-router";

export default defineComponent({
  props: {
    currentPage: {
      type: Number,
      required: true, // Mark it as required
    },
    totalPages: {
      type: Number,
      required: true, // Mark it as required
    },
  },
  emits: ["pageChange"],
  setup(props, { emit }) {
    const router = useRouter();

    const prevPage = () => {
      if (props.currentPage > 1) {
        const page = props.currentPage - 1;
        emit("pageChange", page);
        router.push({ name: "home", query: { page } });
      }
    };

    const nextPage = () => {
      if (props.currentPage < props.totalPages) {
        const page = props.currentPage + 1;
        emit("pageChange", page);
        router.push({ name: "home", query: { page } });
      }
    };

    return {
      prevPage,
      nextPage,
    };
  },
});
</script>
