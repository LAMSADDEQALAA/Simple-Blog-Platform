import Toast from "vue-toastification";

const toast = Toast.useToast();

export const showToast = (message: string, type = "success") => {
  toast(message, { type });
};
