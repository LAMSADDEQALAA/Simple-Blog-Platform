import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "../pages/LoginPage.vue";
import RegisterPage from "../pages/RegisterPage.vue";
import HomePage from "../pages/HomePage.vue";
import PostPage from "../pages/PostPage.vue";
import CreateEditPostPage from "../pages/CreateEditPostPage.vue";
import { useUserStore } from "@/stores/userStore";
import axios from "axios";
const routes = [
  { path: "/login", component: LoginPage },
  { path: "/register", component: RegisterPage },
  {
    path: "/",
    name: "home",
    component: HomePage,
    meta: { requiresAuth: true },
  },
  {
    path: "/posts/:id",
    component: PostPage,
    meta: { requiresAuth: true },
  },
  {
    path: "/posts/create",
    component: CreateEditPostPage,
    meta: { requiresAuth: true },
  },
  {
    path: "/posts/:id/edit",
    component: CreateEditPostPage,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  const isAuthenticated = !!userStore.token;
  const refreshToke = !!userStore.refreshToken;

  if (to.meta.requiresAuth && !isAuthenticated && !refreshToke) {
    next({ path: "/login" });
    return;
  }
  if (to.meta.requiresAuth && !isAuthenticated && refreshToke) {
    axios
      .post(
        `${process.env.VUE_APP_CORE_SERVICE_URL}/api/users/token/refresh/`,
        {
          refresh: userStore.refreshToken,
        }
      )
      .then((response) => {
        userStore.token = response.data.access;
        next("/");
      });
    return;
  }
  next();
});

export default router;
