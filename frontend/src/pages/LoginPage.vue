<template>
  <div class="flex items-center justify-center min-h-screen">
    <div class="max-w-md w-full bg-white shadow-md rounded-lg p-8">
      <h1 class="text-3xl font-bold text-center mb-6">Login</h1>
      <form @submit.prevent="submitForm" class="space-y-4">
        <div>
          <input
            :value="values.username"
            @input="event => setFieldValue('username', (event.target as HTMLInputElement).value)"
            type="text"
            placeholder="Username"
            class="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <span
            v-if="errors.username && isFieldTouched('username')"
            class="text-red-500 text-sm"
          >
            {{ errors.username }}
          </span>
        </div>
        <div>
          <input
            :value="values.password"
            @input="event => setFieldValue('password', (event.target as HTMLInputElement).value)"
            type="password"
            placeholder="Password"
            class="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <span
            v-if="errors.password && isFieldTouched('password')"
            class="text-red-500 text-sm"
          >
            {{ errors.password }}
          </span>
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
import { defineComponent } from "vue";
import { useUserStore } from "@/stores/userStore";
import { useRouter } from "vue-router";
import { useForm } from "vee-validate";
import * as yup from "yup";

export default defineComponent({
  setup() {
    const userStore = useUserStore();
    const router = useRouter();

    const schema = yup.object({
      username: yup.string().required("Username is required"),
      password: yup.string().required("Password is required"),
    });

    const { handleSubmit, errors, values, setFieldValue, isFieldTouched } =
      useForm({
        validationSchema: schema,
      });

    const submitForm = handleSubmit(() => {
      userStore
        .login({
          username: values.username,
          password: values.password,
        })
        .then(() => router.push("/"));
    });

    return {
      submitForm,
      errors,
      values,
      setFieldValue,
      isFieldTouched,
    };
  },
});
</script>
