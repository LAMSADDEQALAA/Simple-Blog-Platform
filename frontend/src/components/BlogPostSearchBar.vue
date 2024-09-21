<template>
  <div class="mb-4">
    <input
      v-model="query"
      @input="onSearch"
      type="text"
      placeholder="Search posts..."
      class="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
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
