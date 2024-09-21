<template>
  <div class="flex items-center justify-center min-h-screen">
    <div class="max-w-md w-full bg-white shadow-md rounded-lg p-8">
      <h1 class="text-3xl font-bold text-center mb-6">Register</h1>
      <form @submit.prevent="registerUser" class="space-y-6">
        <input
          v-model="username"
          type="text"
          placeholder="Username"
          class="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          v-model="password"
          type="password"
          placeholder="Password"
          class="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          v-model="confirmPassword"
          type="password"
          placeholder="Confirm Password"
          class="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          class="bg-blue-500 text-white py-3 px-4 rounded w-full hover:bg-blue-600 transition"
        >
          Register
        </button>
        <p class="text-center text-gray-600">
          Already have an account?
          <router-link to="/login" class="text-blue-500 hover:underline">
            Login
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
    const confirmPassword = ref("");

    const registerUser = async () => {
      await userStore.register({
        username: username.value,
        password: password.value,
      });
      router.push("/login");
    };

    return {
      username,
      confirmPassword,
      password,
      registerUser,
    };
  },
});
</script>
