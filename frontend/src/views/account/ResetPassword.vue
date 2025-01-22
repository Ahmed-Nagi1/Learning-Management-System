<template>
  <main class="min-h-screen flex justify-center items-center bg-base-100 p-6">
    <div class="bg-base-200 p-8 rounded-lg shadow-lg w-full max-w-md">
      <h2 class="text-2xl font-bold mb-6 text-center text-base-content">
        Reset Password
      </h2>
      <form @submit.prevent="resetPassword">
        <div class="mb-4">
          <label
            for="new_password1"
            class="block text-sm font-bold mb-2 text-base-content"
          >
            New Password
          </label>
          <input
            type="password"
            id="new_password1"
            name="new_password1"
            v-model="new_password1"
            required
            placeholder="Enter your new password"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-base-100 text-base-content placeholder-base-content"
          />
        </div>
        <div class="mb-6">
          <label
            for="new_password2"
            class="block text-sm font-bold mb-2 text-base-content"
          >
            Confirm New Password
          </label>
          <input
            type="password"
            id="new_password2"
            name="new_password2"
            v-model="new_password2"
            required
            placeholder="Confirm your new password"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-base-100 text-base-content placeholder-base-content"
          />
        </div>
        <button
          type="submit"
          class="w-full btn btn-primary py-2 px-4 rounded-lg hover:bg-primary-focus focus:outline-none focus:ring-2 focus:ring-primary focus:ring-opacity-50"
        >
          Reset Password
        </button>
      </form>
      <br />
      <p
        v-if="errorMessage"
        class="error-message text-error bg-error bg-opacity-10 px-4 py-2 rounded"
      >
        {{ errorMessage }}
      </p>
      <p
        v-if="successMessage"
        class="success-message text-center text-success bg-success bg-opacity-10 px-4 py-2 rounded"
      >
        {{ successMessage }}
      </p>
      <router-link
        :to="{ name: 'login' }"
        class="block text-center text-primary hover:text-primary-focus mx-auto"
      >
        Login
      </router-link>
    </div>
  </main>
</template>

<script>
import api from "@/api";

export default {
  data() {
    return {
      new_password1: "",
      new_password2: "",
      errorMessage: "",
      successMessage: "",
      uid: this.$route.params.uid,
      token: this.$route.params.token,
    };
  },
  methods: {
    async resetPassword() {
      this.errorMessage = "";
      if (this.new_password1 !== this.new_password2) {
        this.errorMessage = "Passwords do not match";
        return;
      }

      try {
        const response = await api.post("auth/password/reset/confirm/", {
          new_password1: this.new_password1,
          new_password2: this.new_password2,
          uid: this.uid,
          token: this.token,
        });
        this.successMessage = "Password has been reset successfully.";
      } catch (error) {
        this.errorMessage = "";

        if (error.response && error.response.data) {
          const errorData = error.response.data;

          if (errorData.non_field_errors) {
            this.errorMessage = errorData.non_field_errors[0];
          } else {
            for (const field in errorData) {
              if (errorData.hasOwnProperty(field)) {
                const fieldErrors = errorData[field];
                if (fieldErrors.length > 0) {
                  this.errorMessage = `${fieldErrors[0]}`;
                  break;
                }
              }
            }
          }
        } else {
          this.errorMessage = "An unexpected error occurred.";
        }
      }
    },
  },
};
</script>
