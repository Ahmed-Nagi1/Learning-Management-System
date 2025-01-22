<template>
  <main class="bg-base-100 dark:bg-base-300 min-h-screen p-4 sm:p-6">
    <div class="container mx-auto">
      <!-- Error state -->
      <div v-if="error" class="text-center text-error dark:text-error">
        {{ $t('lessonDetail.error') }}
      </div>

      <!-- Display lesson data -->
      <div v-if="lesson">
        <!-- Lesson title -->
        <h1
          class="text-2xl sm:text-3xl font-bold text-center text-base-content dark:text-base-content mb-6 sm:mb-8"
        >
          {{ lesson.title }}
        </h1>

        <!-- Lesson content -->
        <div class="bg-base-200 dark:bg-base-200 rounded-lg shadow-lg p-6">
          <!-- Lesson description -->
          <h2 class="text-lg font-bold text-base-content dark:text-base-content mb-2">
            {{ $t('lessonDetail.description') }}
          </h2>
          <p class="text-base-content dark:text-base-content mb-6 text-sm sm:text-base">
            {{ lesson.description }}
          </p>

          <!-- Divider -->
          <hr class="my-6 border-base-content dark:border-base-content" />

          <!-- Lesson content -->
          <h2 class="text-lg font-bold text-base-content dark:text-base-content mb-2">
            {{ $t('lessonDetail.content') }}
          </h2>
          <div class="prose dark:prose-invert max-w-none text-base-content dark:text-base-content">
            {{ lesson.content }}
          </div>

          <!-- File attachment -->
          <div v-if="lesson.file" class="mt-6">
            <h2 class="text-lg font-bold text-base-content dark:text-base-content mb-2">
              {{ $t('lessonDetail.attachment') }}
            </h2>
            <a
              :href="lesson.file"
              target="_blank"
              class="text-primary dark:text-primary hover:underline"
            >
              {{ $t('lessonDetail.viewFile') }}
            </a>
          </div>

          <!-- Video -->
          <div v-if="lesson.video" class="mt-6">
            <h2 class="text-lg font-bold text-base-content dark:text-base-content mb-2">
              {{ $t('lessonDetail.video') }}
            </h2>
            <video controls class="w-full rounded-lg">
              <source :src="lesson.video" type="video/mp4" />
              {{ $t('lessonDetail.videoNotSupported') }}
            </video>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import api from '@/api';

export default {
  props: ['lesson_id', 'module_id'],
  data() {
    return {
      lesson: null, // Lesson data
      loading: true, // Loading state
      error: null, // Error message
    };
  },
  async created() {
    try {
      // Fetch lesson data from API
      const response = await api.get(`app/lessons/?lesson_id=${this.lesson_id}&module_id=${this.module_id}`); // Replace with your actual API endpoint
      this.lesson = response.data[0]; // Set the received data
    } catch (err) {
      this.error = this.$t('lessonDetail.fetchError'); // Set error message
    } finally {
      this.loading = false; // Stop loading
    }
  },
};
</script>
