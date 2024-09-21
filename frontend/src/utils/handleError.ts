import { isAxiosError } from "axios";
import { notyf } from "./toast";

export const handleError = (error: any) => {
  if (isAxiosError(error)) {
    const status = error.response?.status;
    const data = error.response?.data;

    switch (status) {
      case 400:
        notyf.error("Validation Errors:" + data);
        return data;

      case 401:
        notyf.error("Unauthorized access - possibly expired token.");
        break;

      case 403:
        notyf.error(
          "Forbidden - you don't have permission to access this resource."
        );
        break;

      case 404:
        notyf.error("Not Found - the requested resource could not be found.");
        break;

      case 500:
      case 502:
      case 503:
      case 504:
        notyf.error(
          "Server Error -" + data.detail || "An error occurred on the server."
        );
        break;

      default:
        notyf.error(
          `Error ${status}:` + data.message || "An unexpected error occurred."
        );
        break;
    }
  } else if (error.request) {
    notyf.error("No response received from the server.");
  } else {
    notyf.error("Error:" + error.message);
  }

  return error;
};
