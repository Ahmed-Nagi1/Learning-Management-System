<template>
  <div>
    <!-- زر فتح القائمة الجانبية -->
    <button
      @click="toggleSidebar"
      class="fixed top-4 left-4 z-50 p-3 btn btn-primary rounded-lg shadow-lg hover:bg-primary-focus focus:outline-none focus:ring-2 focus:ring-primary focus:ring-opacity-50 transition-all duration-300"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-5 w-5"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M4 6h16M4 12h16M4 18h16"
        />
      </svg>
    </button>

    <!-- القائمة الجانبية -->
    <div
      :class="[
        'fixed rounded-r-2xl inset-y-0 left-0 w-64 bg-base-200 dark:bg-base-300 shadow-2xl transform transition-transform duration-300 ease-in-out z-40',
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full',
      ]"
    >
      <div class="p-6 mt-10">
        <ul class="space-y-4">
          <li>
            <router-link
              :to="{ name: 'Home' }"
              active-class="active-link"
              class="flex items-center p-3 text-base-content dark:text-base-content hover:bg-base-100 dark:hover:bg-base-100 rounded-lg transition-all duration-200"
            >
              <span class="ml-3">{{ $t('sidebar.home') }}</span>
            </router-link>
          </li>
          <li>
            <router-link
              :to="{ name: 'Dashboard' }"
              active-class="active-link"
              class="flex items-center p-3 text-base-content dark:text-base-content hover:bg-base-100 dark:hover:bg-base-100 rounded-lg transition-all duration-200"
            >
              <span class="ml-3">{{ $t('sidebar.dashboard') }}</span>
            </router-link>
          </li>
          <li>
            <router-link
              :to="{ name: 'EnrollCourses' }"
              active-class="active-link"
              class="flex items-center p-3 text-base-content dark:text-base-content hover:bg-base-100 dark:hover:bg-base-100 rounded-lg transition-all duration-200"
            >
              <span class="ml-3">{{ $t('sidebar.enrollCourses') }}</span>
            </router-link>
          </li>
          <li>
            <router-link
              :to="{ name: 'Settings' }"
              active-class="active-link"
              class="flex items-center p-3 text-base-content dark:text-base-content hover:bg-base-100 dark:hover:bg-base-100 rounded-lg transition-all duration-200"
            >
              <span class="ml-3">{{ $t('sidebar.settings') }}</span>
            </router-link>
          </li>
          <li>
            <a
              href="#"
              class="flex items-center p-3 text-base-content dark:text-base-content hover:bg-base-100 dark:hover:bg-base-100 rounded-lg transition-all duration-200"
            >
              <span class="ml-3">{{ $t('sidebar.contactUs') }}</span>
            </a>
          </li>
        </ul>
      </div>
    </div>

    <!-- خلفية سوداء عند فتح القائمة -->
    <div
      v-if="isSidebarOpen"
      @click="toggleSidebar"
      class="fixed inset-0 bg-black bg-opacity-50 z-30 backdrop-blur-sm"
    ></div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      isSidebarOpen: false,
    };
  },
  methods: {
    toggleSidebar() {
      this.isSidebarOpen = !this.isSidebarOpen;
    },
  },
  watch: {
    $route() {
      this.isSidebarOpen = false;
    },
  },
};
</script>
<style>
.active-link {
  background-color: hsl(var(--p)); /* DaisyUI primary color */
  color: white;
  font-weight: bold;
}
</style>
