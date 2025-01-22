<template>
  <main class="bg-base-300 min-h-screen flex items-center justify-center p-6">
    <div class="w-full max-w-4xl">
      <router-link
        :to="{ name: 'Home' }"
        class="text-base-content hover:text-base-content flex items-center mb-6"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6 mr-2"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M10 19l-7-7m0 0l7-7m-7 7h18"
          />
        </svg>
        {{ $t('infoCourse.backToDashboard') }}
      </router-link>

      <!-- Course Details -->
      <div class="bg-base-200 rounded-lg shadow-lg overflow-hidden">
        <!-- Course Image -->
        <img
          :src="course.image"
          :alt="course.title"
          class="w-full h-64 object-cover cursor-pointer"
          @click="showLightbox"
        />

        <!-- Course Content -->
        <div class="p-6 text-center">
          <h1 class="text-3xl font-bold text-base-content mb-4">
            {{ course.title }}
          </h1>

          <!-- Additional Information -->
          <div class="grid grid-cols-2 gap-6 mb-6">
            <!-- Price -->
            <div>
              <h2 class="text-xl font-bold text-base-content mb-2">
                {{ $t('infoCourse.price') }}
              </h2>
              <p
                class="text-lg"
                :class="course.is_paid ? 'text-primary' : 'text-success'"
              >
                {{ course.is_paid ? `SAR ${course.price}` : $t('infoCourse.free') }}
              </p>
            </div>

            <!-- Number of Students -->
            <div>
              <h2 class="text-xl font-bold text-base-content mb-2">
                {{ $t('infoCourse.students') }}
              </h2>
              <p class="text-lg text-base-content">
                {{ course.students_in_course }}
              </p>
            </div>

            <!-- Rating -->
            <div>
              <h2 class="text-xl font-bold text-base-content mb-2">
                {{ $t('infoCourse.rating') }}
              </h2>
              <p class="text-lg text-warning">{{ course.rating }} / 5</p>
            </div>

            <!-- Status -->
            <div>
              <h2 class="text-xl font-bold text-base-content mb-2">
                {{ $t('infoCourse.status') }}
              </h2>
              <p class="text-lg text-base-content">
                {{ course.is_published ? $t('infoCourse.published') : $t('infoCourse.unpublished') }}
              </p>
            </div>
          </div>

          <!-- Detailed Description -->
          <div class="mt-6 text-left">
            <h2 class="text-xl font-bold text-base-content mb-2">
              {{ $t('infoCourse.description') }}
            </h2>
            <div class="text-base-content text-lg bg-base-100 p-4 rounded-lg">
              {{ course.description || $t('infoCourse.noDescription') }}
            </div>
          </div>

          <!-- Actions -->
          <div class="flex justify-center space-x-4 mt-6">
            <button
              @click="subscribeToCourse"
              class="btn btn-primary hover:bg-primary-focus text-white font-bold py-2 px-4 rounded-lg transition duration-300"
            >
              {{ $t('infoCourse.subscribe') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Lightbox Component -->
    <vue-easy-lightbox
      :visible="visible"
      :imgs="imgs"
      :index="index"
      @hide="handleHide"
    ></vue-easy-lightbox>
  </main>
</template>

<script>
import api from '@/api';
import Swal from 'sweetalert2';
import VueEasyLightbox from 'vue-easy-lightbox';

export default {
  components: {
    VueEasyLightbox,
  },
  data() {
    return {
      course: [],
      isSubscribed: false,
      visible: false,
      imgs: [],
      index: 0,
    };
  },
  methods: {
    async fetchCourse() {
      try {
        const response = await api.get(`/app/courses/${this.$route.params.id}`);
        this.course = response.data;
        this.imgs = [this.course.image]; // Set the image for lightbox
      } catch (e) {
        Swal.fire({
          icon: 'error',
          title: this.$t('infoCourse.errorTitle'),
          text: this.$t('infoCourse.errorText'),
        });
      }
    },
    async subscribeToCourse() {
      try {
        const response = await api.post('/app/enrollment/', {
          course_id: this.$route.params.id,
        });
        if (response.status === 201) {
          this.isSubscribed = true;
          Swal.fire({
            icon: 'success',
            title: this.$t('infoCourse.successTitle'),
            text: this.$t('infoCourse.successText'),
          }).then(() => {
            this.$router.push({ name: 'EnrollCourses' });
          });
        }
      } catch (e) {
        Swal.fire({
          icon: 'error',
          title: this.$t('infoCourse.errorTitle'),
          text: e.response.data.detail,
        });
      }
    },
    showLightbox() {
      this.visible = true;
    },
    handleHide() {
      this.visible = false;
    },
  },
  mounted() {
    this.fetchCourse();
  },
};
</script>