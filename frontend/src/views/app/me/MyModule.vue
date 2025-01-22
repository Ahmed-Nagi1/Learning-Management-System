<template>
  <main class="bg-base-100 dark:bg-base-300 min-h-screen p-4 sm:p-6">
    <div class="container mx-auto">
      <h1
        class="text-2xl sm:text-3xl font-bold text-center text-base-content dark:text-base-content mb-6 sm:mb-8"
      >
        Course Chapters
      </h1>

      <!-- Button to create a new module -->
      <button
        @click="showCreateModuleModal = true"
        class="btn btn-primary px-4 py-2 rounded-lg mb-6 hover:bg-primary-focus transition-colors"
      >
        Create New Module
      </button>

      <!-- Display modules -->
      <div
        class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-4"
      >
        <div
          v-for="module in modules"
          :key="module.id"
          class="bg-base-200 dark:bg-base-200 rounded-lg shadow-lg overflow-hidden transform hover:scale-105 transition-transform duration-300"
        >
          <div class="p-4">
            <h2
              class="text-lg sm:text-xl font-bold text-base-content dark:text-base-content mb-2"
            >
              {{ module.title }}
            </h2>
            <p class="text-base-content dark:text-base-content mb-4 text-xs sm:text-sm">
              {{ module.description }}
            </p>

            <!-- Button to create a new lesson inside the module -->
            <button
              @click="openCreateLessonModal(module.id)"
              class="btn btn-success px-3 py-1 rounded-lg mb-4 hover:bg-success-focus transition-colors"
            >
              Create Lesson
            </button>

            <!-- Display lessons -->
            <div class="space-y-2">
              <div
                v-for="lesson in module.lessons"
                :key="lesson.id"
                class="flex items-center justify-between p-2 bg-base-100 dark:bg-base-100 rounded-lg"
              >
                <span class="text-sm text-base-content dark:text-base-content">{{
                  lesson.title
                }}</span>
                <router-link
                  :to="{
                    name: 'MyLessonDetails',
                    params: { lesson_id: lesson.id, module_id: module.id },
                  }"
                  class="text-primary dark:text-primary text-sm hover:underline"
                >
                  View
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal for creating a new module -->
    <div
      v-if="showCreateModuleModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
    >
      <div class="bg-base-200 dark:bg-base-200 p-6 rounded-lg w-96">
        <h2 class="text-lg font-bold mb-4">Create New Module</h2>
        <input
          v-model="newModule.title"
          type="text"
          placeholder="Module Title"
          class="w-full p-2 mb-4 border rounded-lg bg-base-100 text-base-content dark:bg-base-100 dark:text-base-content"
        />
        <textarea
          v-model="newModule.description"
          placeholder="Module Description"
          class="w-full p-2 mb-4 border rounded-lg bg-base-100 text-base-content dark:bg-base-100 dark:text-base-content"
        ></textarea>
        <div class="flex justify-end">
          <button
            @click="createModule"
            class="btn btn-primary px-4 py-2 rounded-lg hover:bg-primary-focus transition-colors"
          >
            Create
          </button>
          <button
            @click="showCreateModuleModal = false"
            class="ml-2 btn btn-neutral px-4 py-2 rounded-lg hover:bg-neutral-focus transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>

    <!-- Modal for creating a new lesson -->
    <div
      v-if="showCreateLessonModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
    >
      <div class="bg-base-200 dark:bg-base-200 p-6 rounded-lg w-96">
        <h2 class="text-lg font-bold mb-4">Create New Lesson</h2>
        <input
          v-model="newLesson.title"
          type="text"
          placeholder="Lesson Title"
          class="w-full p-2 mb-4 border rounded-lg bg-base-100 text-base-content dark:bg-base-100 dark:text-base-content"
        />
        <input
          v-model="newLesson.description"
          type="text"
          placeholder="Lesson Description"
          class="w-full p-2 mb-4 border rounded-lg bg-base-100 text-base-content dark:bg-base-100 dark:text-base-content"
        />
        <textarea
          v-model="newLesson.content"
          placeholder="Lesson Content"
          class="w-full p-2 mb-4 border rounded-lg bg-base-100 text-base-content dark:bg-base-100 dark:text-base-content"
        ></textarea>
        <input
          type="file"
          @change="handleFileUpload"
          class="w-full p-2 mb-4 border rounded-lg bg-base-100 text-base-content dark:bg-base-100 dark:text-base-content"
        />
        <div class="flex justify-end">
          <button
            @click="createLesson"
            class="btn btn-success px-4 py-2 rounded-lg hover:bg-success-focus transition-colors"
          >
            Create
          </button>
          <button
            @click="showCreateLessonModal = false"
            class="ml-2 btn btn-neutral px-4 py-2 rounded-lg hover:bg-neutral-focus transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import api from "@/api";
import Swal from "sweetalert2";

export default {
  props: ["id"],
  data() {
    return {
      // Modules data
      modules: [],

      // State for creating a new module
      showCreateModuleModal: false,
      newModule: {
        title: "",
        description: "",
      },

      // State for creating a new lesson
      showCreateLessonModal: false,
      newLesson: {
        title: "",
        description: "",
        content: "",
        file: null,
        moduleId: null,
      },
    };
  },
  mounted() {
    // Fetch modules from the API when the page loads
    this.fetchModules();
  },
  methods: {
    // Fetch modules from the API
    async fetchModules() {
      try {
        const response = await api.get(`/app/modules/?pk=${this.id}`);
        this.modules = response.data;
      } catch (error) {
        console.error("Failed to fetch modules:", error);
        Swal.fire({
          icon: "error",
          title: "Error",
          text: "Failed to fetch modules. Please try again later.",
        });
      }
    },

    // Open the modal to create a new lesson
    openCreateLessonModal(moduleId) {
      this.newLesson.moduleId = moduleId;
      this.showCreateLessonModal = true;
    },

    // Handle file upload
    handleFileUpload(event) {
      this.newLesson.file = event.target.files[0];
    },

    // Create a new module
    async createModule() {
      if (this.newModule.title && this.newModule.description) {
        try {
          const response = await api.post(`app/modules/`, {
            course: this.id,
            ...this.newModule,
          });
          this.modules.push(response.data);
          this.newModule.title = "";
          this.newModule.description = "";
          this.showCreateModuleModal = false;

          // Show success message
          Swal.fire({
            icon: "success",
            title: "Success",
            text: "Module created successfully!",
          });
        } catch (error) {
          console.error("Failed to create module:", error);
          Swal.fire({
            icon: "error",
            title: "Error",
            text: "Failed to create module. Please try again.",
          });
        }
      } else {
        Swal.fire({
          icon: "warning",
          title: "Warning",
          text: "Please fill in all fields.",
        });
      }
    },

    // Create a new lesson
    async createLesson() {
      if (this.newLesson.title && this.newLesson.moduleId) {
        try {
          const formData = new FormData();
          formData.append("title", this.newLesson.title);
          formData.append("description", this.newLesson.description);
          formData.append("content", this.newLesson.content);
          formData.append("module", this.newLesson.moduleId);
          if (this.newLesson.file) {
            formData.append("file", this.newLesson.file);
          }

          // إرسال الطلب باستخدام formData
          const response = await api.post(`/app/lessons/`, formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          });

          // تحديث قائمة الدروس في الموديول المحدد
          const module = this.modules.find(
            (m) => m.id === this.newLesson.moduleId
          );
          if (module) {
            module.lessons.push(response.data);
            this.newLesson.title = "";
            this.newLesson.description = "";
            this.newLesson.content = "";
            this.newLesson.file = null;
            this.showCreateLessonModal = false;

            // عرض رسالة نجاح
            Swal.fire({
              icon: "success",
              title: "Success",
              text: "Lesson created successfully!",
            });
          }
        } catch (error) {
          console.error(
            "Failed to create lesson:",
            error.response?.data || error
          );
          Swal.fire({
            icon: "error",
            title: "Error",
            text: "Failed to create lesson. Please try again.",
          });
        }
      } else {
        Swal.fire({
          icon: "warning",
          title: "Warning",
          text: "Please fill in all fields.",
        });
      }
    },
  },
};
</script>

<style scoped>
/* Add custom styles here if needed */
</style>
