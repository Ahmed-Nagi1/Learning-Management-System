<template>
  <main class="bg-base-100 dark:bg-base-300 min-h-screen p-4 sm:p-6">
    <div class="container mx-auto">
      <h1
        class="text-2xl sm:text-3xl font-bold text-center text-base-content dark:text-base-content mb-6 sm:mb-8"
      >
        {{ $t('enrolle.enrolledCourses') }}
      </h1>
      <div
        class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-4"
      >
        <div
          v-for="course in courses"
          :key="course.id"
          class="bg-base-200 dark:bg-base-200 rounded-lg shadow-lg overflow-hidden transform hover:scale-105 transition-transform duration-300"
        >
          <router-link :to="{ name: 'Module', params: { id: course.id } }">
            <img
              :src="course.image"
              :alt="course.title"
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
                <div class="flex items-end">
                  <span
                    class="text-base-content dark:text-base-content text-xs sm:text-sm mr-2"
                  >
                    {{ course.instructorName }}
                  </span>
                  <img
                    :src="course.instructorImage"
                    :alt="course.instructorName"
                    class="w-8 h-8 sm:w-10 sm:h-10 rounded-full object-cover relative top-1"
                  />
                </div>
                <button
                  @click.stop.prevent="confirmDelete(course.ide)"
                  class="text-error hover:text-error focus:outline-none"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-6 w-6"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                    />
                  </svg>
                </button>
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
import Swal from "sweetalert2";

export default {
  data() {
    return {
      courses: [],
    };
  },
  methods: {
    async fetchCourses() {
      try {
        const response = await api.get("/app/enrollment/");
        this.courses = response.data.map((enrollment) => ({
          ide: enrollment.id,
          id: enrollment.course_details.id,
          title: enrollment.course_details.title,
          description: enrollment.course_details.description,
          image: enrollment.course_details.image,
          is_paid: enrollment.course_details.is_paid,
          price: enrollment.course_details.price,
          rating: enrollment.course_details.rating,
          enrolled_at: enrollment.enrolled_at,
          completed: enrollment.completed,
        }));
      } catch (e) {
        console.error("An error occurred while fetching courses:", e);
      }
    },
    async deleteCourse(courseId) {
      try {
        const response = await api.delete(`/app/enrollment/${courseId}/`);
        this.courses = this.courses.filter((course) => course.ide !== courseId);
        if (response.status == 204) {
          Swal.fire(
            this.$t("enrolle.deleteSuccessTitle"),
            this.$t("enrolle.deleteSuccessMessage"),
            "success"
          );
        }
      } catch (e) {
        Swal.fire(
          this.$t("enrolle.deleteErrorTitle"),
          this.$t("enrolle.deleteErrorMessage"),
          "error"
        );
      }
    },
    confirmDelete(courseId) {
      Swal.fire({
        title: this.$t("enrolle.confirmDeleteTitle"),
        text: this.$t("enrolle.confirmDeleteText"),
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: this.$t("enrolle.confirmButtonText"),
        cancelButtonText: this.$t("enrolle.cancelButtonText"),
      }).then((result) => {
        if (result.isConfirmed) {
          this.deleteCourse(courseId);
        }
      });
    },
  },
  mounted() {
    this.fetchCourses();
  },
};
</script>
