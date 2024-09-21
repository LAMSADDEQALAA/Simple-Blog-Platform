import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import Toast, { POSITION } from "vue-toastification";

const app = createApp(App);

const pinia = createPinia();

app.use(pinia);
app.use(Toast, {
  position: POSITION.TOP_RIGHT,
  timeout: 5000,
});
app.use(router);

app.mount("#app");
