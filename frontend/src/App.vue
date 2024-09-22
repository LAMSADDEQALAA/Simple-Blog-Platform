<template>
  <div class="min-h-screen bg-gray-100">
    <nav class="bg-gray-800 p-4 shadow-lg">
      <div class="container mx-auto flex justify-between items-center">
        <div class="text-white text-lg font-semibold">
          <router-link to="/">Blog</router-link>
        </div>
        <div class="space-x-4">
          <router-link
            v-if="!isAuthenticated"
            to="/login"
            class="text-white hover:bg-gray-700 rounded px-3 py-2 transition"
            >Login</router-link
          >
          <router-link
            v-if="!isAuthenticated"
            to="/register"
            class="text-white hover:bg-gray-700 rounded px-3 py-2 transition"
            >Register</router-link
          >
          <button
            v-if="isAuthenticated"
            @click="logout"
            class="text-white hover:bg-gray-700 rounded px-3 py-2 transition"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script lang="ts">
import { computed, defineComponent } from "vue";
import { useUserStore } from "@/stores/userStore";
import { useRouter } from "vue-router";
import { notyf } from "./utils/toast";

export default defineComponent({
  setup() {
    const userStore = useUserStore();
    const isAuthenticated = computed(() => !!userStore.token);
    const router = useRouter();

    if (!isAuthenticated.value) {
      router.push("/login");
    }
    const logout = () => {
      userStore.logout();
      router.push("/login");
      notyf.success("loged out successfuly!");
    };

    return { isAuthenticated, logout };
  },
});
</script>

<style scoped>
/* Additional styles can go here if needed */
</style>
