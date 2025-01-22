<template>
  <main class="min-h-screen flex justify-center items-center bg-base-100 p-6">
    <div class="bg-base-200 p-8 rounded-lg shadow-lg w-full max-w-md">
      <h2 class="text-2xl font-bold mb-6 text-center text-base-content">
        Sign Up
      </h2>
      <form @submit.prevent="signup">
        <div class="mb-4">
          <label
            for="full_name"
            class="block text-sm font-bold mb-2 text-base-content"
          >
            Full Name
          </label>
          <input
            type="text"
            id="full_name"
            name="full_name"
            v-model="full_name"
            required
            placeholder="Enter your full name"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-base-100 text-base-content placeholder-base-content"
          />
        </div>
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
        <div class="mb-4">
          <label
            for="password1"
            class="block text-sm font-bold mb-2 text-base-content"
          >
            Password
          </label>
          <input
            type="password"
            id="password1"
            name="password1"
            v-model="password1"
            required
            placeholder="Enter your password"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-base-100 text-base-content placeholder-base-content"
          />
        </div>
        <div class="mb-6">
          <label
            for="password2"
            class="block text-sm font-bold mb-2 text-base-content"
          >
            Confirm Password
          </label>
          <input
            type="password"
            id="password2"
            name="password2"
            v-model="password2"
            required
            placeholder="Confirm your password"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-base-100 text-base-content placeholder-base-content"
          />
        </div>
        <button
          type="submit"
          class="w-full btn btn-primary py-2 px-4 rounded-lg hover:bg-primary-focus focus:outline-none focus:ring-2 focus:ring-primary focus:ring-opacity-50"
        >
          Sign Up
        </button>
      </form>
      <br />
      <p
        v-if="errorMessage"
        class="error-message text-center text-error bg-error bg-opacity-10 px-4 py-2 rounded"
      >
        {{ errorMessage }}
      </p>
      <p
        v-if="successMessage"
        class="success-message text-center text-success bg-success bg-opacity-10 px-4 py-2 rounded"
      >
        {{ successMessage }}
      </p>
      <div class="mt-6 text-center">
        <p class="text-sm text-base-content">
          Already have an account?
          <router-link
            :to="{ name: 'login' }"
            class="text-primary hover:text-primary-focus"
          >
            Login
          </router-link>
        </p>
      </div>
    </div>
  </main>
</template>

<script>
import api from "@/api";

export default {
  data() {
    return {
      full_name: "",
      email: "",
      password1: "",
      password2: "",
      errorMessage: "",
      successMessage: "",
    };
  },
  methods: {
    async signup() {
      this.errorMessage = "";
      if (this.password1 !== this.password2) {
        this.errorMessage = "Passwords do not match";
        return;
      }

      try {
        const response = await api.post("auth/registration/", {
          full_name: this.full_name,
          email: this.email,
          password1: this.password1,
          password2: this.password2,
        });
        this.successMessage = response.data.detail;
      } catch (error) {
        this.errorMessage = "";
        if (error.response?.data) {
          const errorData = error.response.data;
          this.errorMessage =
            errorData.non_field_errors?.[0] ||
            Object.values(errorData).flat()?.[0] ||
            "An unexpected error occurred.";
        } else {
          this.errorMessage = "An unexpected error occurred.";
        }
      }
    },
  },
};
</script>
