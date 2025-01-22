<template>
  <main
    class="bg-gray-100 dark:bg-gray-900 min-h-screen p-6 flex justify-center items-center"
  >
    <div
      v-if="!loading"
      class="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-lg w-full max-w-md text-center"
    >
      <div class="flex justify-center mb-4">
        <div
          class="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center"
          v-if="!errorMessage"
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
        <p
          v-if="errorMessage"
          class="error-message text-red-500 bg-red-500 bg-opacity-10 px-4 py-2 rounded"
        >
          {{ errorMessage }}
        </p>
      </div>

      <h2
        class="text-2xl font-bold mb-4 text-gray-800 dark:text-gray-100"
        v-if="!errorMessage"
      >
        Email Confirmed Successfully!
      </h2>
      <h2
        class="text-2xl font-bold mb-4 text-red-600 dark:text-red-400"
        v-if="errorMessage"
      >
        Error Confirming Email
      </h2>

      <p class="text-gray-600 dark:text-gray-400" v-if="!errorMessage">
        You will be redirected to the login page in {{ countdown }} seconds...
      </p>
      <p class="text-gray-600 dark:text-gray-400" v-if="errorMessage">
        Please try again later or contact support.
      </p>
    </div>
    <div v-else class="text-center text-gray-600 dark:text-gray-400">
      Loading, please wait...
    </div>
  </main>
</template>

<script>
import api from "@/api";

export default {
  data() {
    return {
      countdown: 5,
      errorMessage: null,
      loading: true, // Initial loading state
    };
  },
  methods: {
    async ConfirmEmail() {
      try {
        const response = await api.post(
          "/auth/registration/account-confirm-email/", 
          {"key":this.$route.params.key}, 
        );

        // localStorage.setItem("email", response.data.email);

        this.loading = false;
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
        this.loading = false;
      }
    },
  },
  mounted() {
    this.ConfirmEmail();

    if (!this.errorMessage) {
      const timer = setInterval(() => {
        this.countdown--;
        if (this.countdown === 0) {
          clearInterval(timer);
          this.$router.push({ name: "login" });
        }
      }, 1000);
    }
  },
};
</script>
