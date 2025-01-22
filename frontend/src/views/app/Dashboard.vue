<template>
  <main class="bg-base-300 min-h-screen">
    <!-- شريط التنقل العلوي -->
    <nav class="bg-base-200 shadow-md relative">
      <div
        class="container mx-auto px-6 py-4 flex justify-between items-center"
      >
        <!-- كلمة "لوحة التحكم" في المنتصف -->
        <h1
          class="absolute left-0 right-0 text-2xl font-bold text-base-content text-center"
        >
          {{ $t("dashboard.title") }}
        </h1>
        <div class="flex items-center space-x-4 ml-auto">
          <span class="text-base-content font-medium" v-text="owner_name"></span>
          <img
            loading="lazy"
            :src="owner_image"
            alt="profile"
            class="w-10 h-10 rounded-full"
          />
        </div>
      </div>
    </nav>

    <!-- المحتوى الرئيسي -->
    <div class="container mx-auto px-6 py-8">
      <!-- بطاقة إنشاء دورة جديدة -->
      <router-link
        :to="{ name: 'CreateCourse' }"
        class="block bg-base-200 p-6 rounded-lg shadow-md transform hover:scale-105 transition-transform duration-300 mb-8"
      >
        <div class="flex items-center justify-center space-x-4">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-12 w-12 text-primary"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 6v6m0 0v6m0-6h6m-6 0H6"
            />
          </svg>
          <h2 class="text-xl font-bold text-base-content">
            {{ $t("dashboard.createNewCourse") }}
          </h2>
        </div>
        <p class="text-base-content text-center mt-2">
          {{ $t("dashboard.createCourseDescription") }}
        </p>
      </router-link>

      <!-- إحصائيات -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-base-200 p-6 rounded-lg shadow-md">
          <h2 class="text-lg font-bold text-base-content">
            {{ $t("dashboard.numberOfCourses") }}
          </h2>
          <p
            class="text-3xl font-bold text-primary mt-2"
            v-text="courseCount"
          ></p>
        </div>

        <div class="bg-base-200 p-6 rounded-lg shadow-md">
          <h2 class="text-lg font-bold text-base-content">
            {{ $t("dashboard.totalRevenue") }}
          </h2>
          <p class="text-3xl font-bold text-success mt-2">SAR 5,400</p>
        </div>

        <div class="bg-base-200 p-6 rounded-lg shadow-md">
          <h2 class="text-lg font-bold text-base-content">
            {{ $t("dashboard.numberOfStudents") }}
          </h2>
          <p class="text-3xl font-bold text-secondary mt-2">
            {{ allStudents }}
          </p>
        </div>
      </div>

      <!-- قائمة الدورات التدريبية -->
      <div class="mt-8">
        <h2 class="text-2xl font-bold text-base-content mb-6">
          {{ $t("dashboard.myTrainingCourses") }}
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="course in courses"
            :key="course.id"
            class="bg-base-200 rounded-lg shadow-md overflow-hidden transform hover:scale-105 transition-transform duration-300"
          >
            <router-link
              :to="{ name: 'InfoMyCourse', params: { id: course.id } }"
            >
              <img
                loading="lazy"
                :src="course.image"
                :alt="course.name"
                class="w-full h-48 object-cover"
              />
              <div class="p-6">
                <h3 class="text-xl font-bold text-base-content mb-2">
                  {{ course.name }}
                </h3>
                <p class="text-base-content text-sm mb-4">
                  {{ course.description }}
                </p>
                <div class="flex justify-between items-center">
                  <span
                    class="text-lg font-bold"
                    :class="course.is_paid ? 'text-primary' : 'text-success'"
                  >
                    {{
                      course.is_paid
                        ? `SAR ${course.price}`
                        : $t("dashboard.free")
                    }}
                  </span>
                  <span class="text-sm text-base-content">
                    {{ course.students }} {{ $t("dashboard.students") }}
                  </span>
                </div>
              </div>
            </router-link>
          </div>
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
      courses: null,
      courseCount: null,
      allStudents: null,
      owner_name: null,
      owner_image: null,
    };
  },
  methods: {
    async fetchCourses() {
      try {
        const response = await api.get("/app/courses/my-courses/");
        this.courses = response.data.courses;
        this.allStudents = response.data.total_students;
        this.courseCount = response.data.courses.length;

        if (this.courses.length > 0) {
          this.owner_name = this.courses[0].owner_name;
          this.owner_image = this.courses[0].owner_image;
        }
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
