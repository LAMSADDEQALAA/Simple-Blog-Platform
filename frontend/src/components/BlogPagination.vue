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
  methods: {
    prevPage() {
      if (this.currentPage > 1) this.$emit("pageChange", this.currentPage - 1);
    },
    nextPage() {
      if (this.currentPage < this.totalPages)
        this.$emit("pageChange", this.currentPage + 1);
    },
  },
});
</script>
