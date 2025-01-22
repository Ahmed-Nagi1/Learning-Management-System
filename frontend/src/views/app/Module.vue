<template>
  <main class="bg-base-100 dark:bg-base-300 min-h-screen p-4 sm:p-6">
    <div class="container mx-auto">
      <h1
        class="text-2xl sm:text-3xl font-bold text-center text-base-content dark:text-base-content mb-6 sm:mb-8"
      >
        {{ $t('module.title') }}
      </h1>
      <div
        class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-4"
      >
        <div
          v-for="chapter in chapters"
          :key="chapter.id"
          class="bg-base-200 dark:bg-base-200 rounded-lg shadow-lg overflow-hidden transform hover:scale-105 transition-transform duration-300"
        >
          <div class="p-4">
            <h2
              class="text-lg sm:text-xl font-bold text-base-content dark:text-base-content mb-2"
            >
              {{ chapter.title }}
            </h2>
            <p class="text-base-content dark:text-base-content mb-4 text-xs sm:text-sm">
              {{ chapter.description }}
            </p>
            <div class="space-y-2">
              <div
                v-for="lesson in chapter.lessons"
                :key="lesson.id"
                class="flex items-center justify-between p-2 bg-base-100 dark:bg-base-100 rounded-lg"
              >
                <div class="flex flex-col">
                  <span class="text-sm text-base-content dark:text-base-content">
                    {{ lesson.title }}
                  </span>
                  <span class="text-xs text-base-content dark:text-base-content">
                    {{ lesson.description }}
                  </span>
                </div>
                <router-link
                  :to="{ 
                    name: 'LessonDetails',
                    params: { lesson_id: lesson.id, module_id: chapter.id }
                  }"
                  class="text-primary dark:text-primary text-sm hover:underline"
                >
                  {{ $t('module.viewButton') }}
                </router-link>
              </div>
            </div>
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
      chapters: [],
    };
  },
  methods: {
    async fetchChapters() {
      try {
        const response = await api.get(
          `/app/modules/?pk=${this.$route.params.id}`
        );
        this.chapters = response.data;
      } catch (e) {
        console.error(this.$t("module.errorMessage"), e);
      }
    },
  },
  mounted() {
    this.fetchChapters();
  },
};
</script>
