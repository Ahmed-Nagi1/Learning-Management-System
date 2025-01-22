<template>
  <main class="min-h-screen flex justify-center items-center bg-base-100 p-6">
    <div class="bg-base-200 p-8 rounded-lg shadow-lg w-full max-w-md">
      <h2 class="text-2xl font-bold mb-6 text-center text-base-content">
        Change Email
      </h2>
      <h3 class="bg-info text-info-content text-center text-lg font-semibold p-4 rounded">
        {{ getEmailData }}
      </h3>

      <form @submit.prevent="resetPassword">
        <div class="mb-4">
          <label for="email" class="block text-sm font-bold mb-2 text-base-content">
            New Email
          </label>
          <input
            type="email"
            id="email"
            name="email"
            v-model="email"
            required
            placeholder="Enter your new email"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-base-100 text-base-content placeholder-base-content"
          />
        </div>
        <button
          type="submit"
          class="w-full btn btn-primary py-2 px-4 rounded-lg hover:bg-primary-focus focus:outline-none focus:ring-2 focus:ring-primary focus:ring-opacity-50"
        >
          Change Email
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
        :to="{ name: 'changePassword' }"
        class="block text-center text-primary hover:text-primary-focus mx-auto"
      >
        Change Password
      </router-link>
      <router-link
        :to="{ name: 'login' }"
        class="block text-center text-primary hover:text-primary-focus mx-auto"
      >
        Back
      </router-link>
    </div>
  </main>
</template>

<script>
import api from "@/api";

export default {
  data() {
    return {
      email: "",
      errorMessage: null,
      successMessage: null,
    };
  },
  computed: {
    getEmailData() {
      const data = localStorage.getItem("email");
      return data ? data : "No data available";
    },
  },
  methods: {
    async resetPassword() {
      this.errorMessage = null;
      this.successMessage = null;

      if (!this.email) {
        this.errorMessage = "Please enter a valid email.";
        return;
      }

      try {
        const response = await api.post("/auth/change-email/", {
          email: this.email,
        });
        this.successMessage = response.data.message;
      } catch (error) {
        this.errorMessage = "An unexpected error occurred.";
        if (error.response && error.response.data) {
          const errorData = error.response.data;
          if (errorData.non_field_errors) {
            this.errorMessage = errorData.non_field_errors[0];
          } else {
            for (const field in errorData) {
              if (errorData.hasOwnProperty(field)) {
                const fieldErrors = errorData[field];
                if (fieldErrors.length > 0) {
                  this.errorMessage = fieldErrors[0];
                  break;
                }
              }
            }
          }
        }
      }
    },
  },
};
</script>