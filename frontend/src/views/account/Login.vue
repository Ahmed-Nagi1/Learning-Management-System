<template>
  <main class="min-h-screen flex justify-center items-center bg-base-100 p-6">
    <div class="bg-base-200 p-8 rounded-lg shadow-lg w-full max-w-md">
      <h2 class="text-2xl font-bold mb-6 text-center text-base-content">
        Login
      </h2>
      <form @submit.prevent="login">
        <div class="mb-4">
          <label for="email" class="block text-sm font-bold mb-2 text-base-content">
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
        <div class="mb-6">
          <label for="password" class="block text-sm font-bold mb-2 text-base-content">
            Password
          </label>
          <input
            type="password"
            id="password"
            name="password"
            v-model="password"
            required
            placeholder="Enter your password"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-base-100 text-base-content placeholder-base-content"
          />
        </div>
        <button
          type="submit"
          class="w-full btn btn-primary py-2 px-4 rounded-lg hover:bg-primary-focus focus:outline-none focus:ring-2 focus:ring-primary focus:ring-opacity-50"
        >
          Login
        </button>
      </form>
      <br>
      <p
        v-if="errorMessage"
        class="error-message text-center text-error bg-error bg-opacity-10 px-4 py-2 rounded"
      >
        {{ errorMessage }}
      </p>
      <div class="mt-6 text-center">
        <router-link
          :to="{name:'forgetPassword'}"
          class="text-sm text-primary hover:text-primary-focus"
        >
          Forgot your password?
        </router-link>
      </div>
      <div class="mt-4 text-center">
        <p class="text-sm text-base-content">
          Don't have an account?
          <router-link
            :to="{name:'signup'}"
            class="text-primary hover:text-primary-focus"
          >
            Sign up
          </router-link>
        </p>
      </div>
    </div>
  </main>
</template>

<script>
import api from '@/api';

export default {
  data() {
    return {
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await api.post(
          "/auth/login/", 
          {
            email: this.email,
            password: this.password,
          }
        );

        const accessToken = response.data.access;
        const refreshToken = response.data.refresh;
        const email = response.data.user.email;
        localStorage.setItem("accessToken", accessToken);
        localStorage.setItem("refreshToken", refreshToken);
        localStorage.setItem("email", email);

        this.$router.push("/");
      } catch (error) {
        this.errorMessage = error?.response?.data?.detail || "An unexpected error occurred.";
      }
    },
  },
};
</script>