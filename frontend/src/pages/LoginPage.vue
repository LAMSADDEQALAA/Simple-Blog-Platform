<template>
  <div class="flex items-center justify-center min-h-screen">
    <div class="max-w-md w-full bg-white shadow-md rounded-lg p-8">
      <h1 class="text-3xl font-bold text-center mb-6">Login</h1>
      <form @submit.prevent="loginUser" class="space-y-4">
        <div>
          <input
            v-model="username"
            type="text"
            placeholder="Username"
            class="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div>
          <input
            v-model="password"
            type="password"
            placeholder="Password"
            class="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <button
          type="submit"
          class="bg-blue-600 text-white py-3 rounded w-full hover:bg-blue-700 transition duration-200"
        >
          Login
        </button>
        <p class="text-center">
          Don't have an account?
          <router-link to="/register" class="text-blue-600 hover:underline">
            Register
          </router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useUserStore } from "@/stores/userStore";
import { useRouter } from "vue-router";

export default defineComponent({
  setup() {
    const userStore = useUserStore();
    const router = useRouter();

    const username = ref("");
    const password = ref("");

    const loginUser = async () => {
      await userStore.login({
        username: username.value,
        password: password.value,
      });
      await userStore.getUserData();

      router.push("/");
    };

    return {
      username,
      password,
      loginUser,
    };
  },
});
</script>
