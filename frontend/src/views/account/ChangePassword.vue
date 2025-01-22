<template>
  <main class="min-h-screen flex justify-center items-center bg-base-100 p-6">
    <div
      v-if="!successPage"
      class="bg-base-200 p-8 rounded-lg shadow-lg w-full max-w-md"
    >
      <h2 class="text-2xl font-bold mb-6 text-center text-base-content">
        Change Password
      </h2>
      <form @submit.prevent="resetPassword">
        <div class="mb-4">
          <label
            for="old_password"
            class="block text-sm font-bold mb-2 text-base-content"
          >
            Old Password
          </label>
          <input
            type="password"
            id="old_password"
            name="old_password"
            v-model="old_password"
            required
            placeholder="Enter your old password"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-base-100 text-base-content placeholder-base-content"
          />
        </div>
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
      <div>
        <router-link
          :to="{ name: 'forgetPassword' }"
          class="block text-center text-primary hover:text-primary-focus mx-auto"
        >
          Forget Password
        </router-link>
      </div>
      <router-link
        :to="{ name: 'login' }"
        class="block text-center text-primary hover:text-primary-focus mx-auto"
      >
        Back
      </router-link>
    </div>
    <div
      v-if="successPage"
      class="bg-base-200 p-8 rounded-lg shadow-lg w-full max-w-md text-center"
    >
      <div class="flex justify-center mb-4">
        <div
          class="w-16 h-16 bg-success rounded-full flex items-center justify-center"
        >
          <svg
            class="w-10 h-10 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M5 13l4 4L19 7"
            ></path>
          </svg>
        </div>
      </div>
      <h2 class="text-2xl font-bold mb-4 text-base-content">
        Password Changed Successfully!
      </h2>
      <p class="text-base-content">
        You will be redirected to the login page in {{ countdown }} seconds...
      </p>
    </div>
  </main>
</template>

<script>
import api from "@/api";

export default {
  data() {
    return {
      old_password: "",
      new_password1: "",
      new_password2: "",
      errorMessage: "",
      successMessage: "",
      successPage: false,
      countdown: 5, // Countdown timer
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
        const response = await api.post("/auth/password/change/", {
          old_password: this.old_password,
          new_password1: this.new_password1,
          new_password2: this.new_password2,
        });
        this.successPage = true;

        // Countdown and redirect
        const interval = setInterval(() => {
          this.countdown--;
          if (this.countdown === 0) {
            clearInterval(interval);
            this.$router.push({ name: "login" });
          }
        }, 1000); // Update countdown every second
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