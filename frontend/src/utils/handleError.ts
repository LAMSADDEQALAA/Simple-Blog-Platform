import { isAxiosError } from "axios";
import { showToast } from "./toast";

export const handleError = (error: any) => {
  if (isAxiosError(error)) {
    const status = error.response?.status;
    const data = error.response?.data;

    switch (status) {
      case 400:
        showToast("Validation Errors:" + data, "error");
        return data;

      case 401:
        showToast("Unauthorized access - possibly expired token.", "error");
        break;

      case 403:
        showToast(
          "Forbidden - you don't have permission to access this resource.",
          "error"
        );
        break;

      case 404:
        showToast(
          "Not Found - the requested resource could not be found.",
          "error"
        );
        break;

      case 500:
      case 502:
      case 503:
      case 504:
        showToast(
          "Server Error -" + data.detail || "An error occurred on the server.",
          "error"
        );
        break;

      default:
        showToast(
          `Error ${status}:` + data.message || "An unexpected error occurred.",
          "error"
        );
        break;
    }
  } else if (error.request) {
    showToast("No response received from the server.", "error");
  } else {
    showToast("Error:", error.message);
  }

  return error;
};
