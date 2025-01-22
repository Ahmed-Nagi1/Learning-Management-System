<template>
  <main class="min-h-screen flex justify-center items-center bg-base-100 p-6">
    <div class="bg-base-200 p-8 rounded-lg shadow-lg w-full max-w-md">
      <h2 class="text-2xl font-bold mb-6 text-center text-base-content">
        Reset Password
      </h2>
      <form @submit.prevent="ResetPassword">
        <div class="mb-4">
          <label
            for="email"
            class="block text-sm font-bold mb-2 text-base-content"
          >
            Email
          </label>
          <input
            type="email"
            id="email"
            name="email"
            v-model="email"
            required
            placeholder="Enter your email"
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
        v-if="successMessage"
        class="success-message text-success bg-success bg-opacity-10 px-4 py-2 rounded"
      >
        {{ successMessage }}
      </p>
    </div>
  </main>
</template>

<script>
import api from "@/api";

export default {
  data() {
    return {
      email: "",
      successMessage: "",
    };
  },
  methods: {
    async ResetPassword() {
      try {
        const response = await api.post("/auth/password/reset/", {
          email: this.email,
        });

        this.successMessage = response.data.detail;
      } catch (error) {
        // Handle error if needed
      }
    },
  },
};
</script>