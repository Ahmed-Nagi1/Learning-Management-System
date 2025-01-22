<template>
  <main class="bg-base-100 dark:bg-base-300 min-h-screen p-4 sm:p-6">
    <div class="container mx-auto">
      <h1
        class="text-2xl sm:text-3xl font-bold text-center text-base-content dark:text-base-content mb-6 sm:mb-8"
      >
        Our Courses
      </h1>
      <div
        class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-4"
      >
        <div
          v-for="course in courses"
          :key="course.id"
          class="bg-base-200 dark:bg-base-200 rounded-lg shadow-lg overflow-hidden transform hover:scale-105 transition-transform duration-300"
        >
          <router-link :to="{ name: 'InfoCourse', params: { id: course.id } }">
            <img
              :src="course.image"
              :alt="course.title"
              loading="lazy"
              class="w-full h-32 sm:h-48 object-cover"
            />
            <div class="p-4">
              <h2
                class="text-lg sm:text-xl font-bold text-base-content dark:text-base-content mb-2"
              >
                {{ course.title }}
              </h2>
              <p
                class="text-base-content dark:text-base-content mb-4 text-xs sm:text-sm"
              >
                {{ course.description }}
              </p>
              <div class="flex justify-between items-end">
                <span
                  class="text-base sm:text-lg font-bold text-primary dark:text-primary"
                  >{{ course.price }}</span
                >
                <div class="flex items-end">
                  <span
                    class="text-base-content dark:text-base-content text-xs sm:text-sm mr-2"
                    >{{ course.owner_name }}</span
                  >
                  <img
                    :src="course.owner_image"
                    :alt="course.owner_name"
                    class="w-8 h-8 sm:w-10 sm:h-10 rounded-full object-cover relative top-1"
                  />
                </div>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </main>
</template>
<script>
import api from "@/api";
export default {
  data() {
    return {
      courses: [],
    };
  },
  methods: {
    async fetchCourses() {
      try {
        const response = await api.get("/app/courses/");
        this.courses = response.data;
      } catch (e) {
        console.error("An error occurred while fetching courses:", e);
      }
    },
  },
  mounted() {
    this.fetchCourses();
  },
};
</script>
