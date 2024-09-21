<template>
  <div class="mb-4">
    <input
      v-model="query"
      @input="onSearch"
      type="text"
      placeholder="Search posts..."
      class="w-full p-2 border border-gray-300 rounded"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { debounce } from "lodash";

export default defineComponent({
  emits: ["search"],
  setup(_, { emit }) {
    const query = ref("");

    const debouncedSearch = debounce((value: string) => {
      emit("search", value);
    }, 500);

    const onSearch = () => {
      debouncedSearch(query.value);
    };

    return {
      query,
      onSearch,
    };
  },
});
</script>

<style scoped>
/* Style the search input using Tailwind CSS */
input {
  @apply w-full p-2 border border-gray-300 rounded;
}
</style>
