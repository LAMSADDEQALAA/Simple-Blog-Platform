<template>
  <div>
    <nav class="bg-gray-800 p-4">
      <div class="container mx-auto flex justify-between">
        <div>
          <router-link to="/" class="text-white">Home</router-link>
        </div>
        <div>
          <router-link v-if="!isAuthenticated" to="/login" class="text-white"
            >Login</router-link
          >
          <router-link v-if="!isAuthenticated" to="/register" class="text-white"
            >Register</router-link
          >
          <button v-if="isAuthenticated" @click="logout" class="text-white">
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
    };

    return { isAuthenticated, logout };
  },
});
</script>

<style>
@tailwind base;
@tailwind components;
@tailwind utilities;

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
