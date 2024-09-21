<template>
  <div class="max-w-md mx-auto mt-10">
    <h1 class="text-2xl font-bold mb-4">Register</h1>
    <form @submit.prevent="registerUser" class="space-y-4">
      <input
        v-model="username"
        type="text"
        placeholder="Username"
        class="w-full p-2 border border-gray-300 rounded"
      />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="w-full p-2 border border-gray-300 rounded"
      />
      <input
        v-model="confirmPassword"
        type="password"
        placeholder="confirm Password"
        class="w-full p-2 border border-gray-300 rounded"
      />
      <button
        type="submit"
        class="bg-blue-500 text-white py-2 px-4 rounded w-full"
      >
        Register
      </button>
      <router-link to="/login" class="text-white">login</router-link>
    </form>
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
