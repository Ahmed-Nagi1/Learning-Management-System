<template>
  <main class="bg-base-100 dark:bg-base-300 min-h-screen p-4 sm:p-6">
    <div class="container mx-auto">
      <!-- Error state -->
      <div v-if="error" class="text-center text-error dark:text-error">
        {{ error }}
      </div>

      <!-- Display lesson data -->
      <div v-if="lesson">
        <!-- Lesson title -->
        <h1
          class="text-2xl sm:text-3xl font-bold text-center text-base-content dark:text-base-content mb-6 sm:mb-8"
        >
          {{ lesson.title }}
        </h1>

        <!-- Edit and Delete buttons -->
        <div class="text-right mb-4 space-x-2">
          <button
            @click="openEditModal"
            class="btn btn-primary px-4 py-2 rounded-lg hover:bg-primary-focus transition duration-300"
          >
            Edit Lesson
          </button>
          <button
            @click="confirmDelete"
            class="btn btn-error px-4 py-2 rounded-lg hover:bg-error-focus transition duration-300"
          >
            Delete Lesson
          </button>
        </div>

        <!-- Lesson content -->
        <div class="bg-base-200 dark:bg-base-200 rounded-lg shadow-lg p-6">
          <!-- Lesson description -->
          <h2 class="text-lg font-bold text-base-content dark:text-base-content mb-2">
            Lesson Description
          </h2>
          <p class="text-base-content dark:text-base-content mb-6 text-sm sm:text-base">
            {{ lesson.description }}
          </p>

          <!-- Divider -->
          <hr class="my-6 border-base-content dark:border-base-content" />

          <!-- Lesson content -->
          <h2 class="text-lg font-bold text-base-content dark:text-base-content mb-2">
            Lesson Content
          </h2>
          <div class="prose dark:prose-invert max-w-none text-base-content dark:text-base-content">
            {{ lesson.content }}
          </div>

          <!-- File attachment -->
          <div v-if="lesson.file" class="mt-6">
            <h2 class="text-lg font-bold text-base-content dark:text-base-content mb-2">
              Attached File
            </h2>
            <a
              :href="lesson.file"
              target="_blank"
              class="text-primary dark:text-primary hover:underline"
            >
              View File
            </a>
          </div>

          <!-- Video -->
          <div v-if="lesson.video" class="mt-6">
            <h2 class="text-lg font-bold text-base-content dark:text-base-content mb-2">
              Video
            </h2>
            <video controls class="w-full rounded-lg">
              <source :src="lesson.video" type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>
        </div>
      </div>

      <!-- Edit Modal -->
      <div v-if="isEditModalOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
        <div class="bg-base-200 dark:bg-base-200 rounded-lg shadow-lg p-6 w-full max-w-2xl">
          <h2 class="text-xl font-bold text-base-content dark:text-base-content mb-4">Edit Lesson</h2>

          <!-- Edit Form -->
          <form @submit.prevent="submitEdit">
            <div class="mb-4">
              <label class="block text-base-content dark:text-base-content mb-2">Title</label>
              <input
                v-model="editedLesson.title"
                class="w-full px-4 py-2 border rounded-lg bg-base-100 text-base-content dark:bg-base-100 dark:text-base-content"
              />
            </div>

            <div class="mb-4">
              <label class="block text-base-content dark:text-base-content mb-2">Description</label>
              <textarea
                v-model="editedLesson.description"
                class="w-full px-4 py-2 border rounded-lg bg-base-100 text-base-content dark:bg-base-100 dark:text-base-content"
              ></textarea>
            </div>

            <div class="mb-4">
              <label class="block text-base-content dark:text-base-content mb-2">Content</label>
              <textarea
                v-model="editedLesson.content"
                class="w-full px-4 py-2 border rounded-lg bg-base-100 text-base-content dark:bg-base-100 dark:text-base-content"
              ></textarea>
            </div>

            <!-- File Upload -->
            <div class="mb-4">
              <label class="block text-base-content dark:text-base-content mb-2">Upload File</label>
              <input
                type="file"
                @change="handleFileUpload"
                class="w-full px-4 py-2 border rounded-lg bg-base-100 text-base-content dark:bg-base-100 dark:text-base-content"
              />
            </div>

            <!-- Video Upload -->
            <div class="mb-4">
              <label class="block text-base-content dark:text-base-content mb-2">Upload Video</label>
              <input
                type="file"
                @change="handleVideoUpload"
                class="w-full px-4 py-2 border rounded-lg bg-base-100 text-base-content dark:bg-base-100 dark:text-base-content"
              />
            </div>

            <div class="flex justify-end">
              <button
                type="button"
                @click="closeEditModal"
                class="btn btn-neutral px-4 py-2 rounded-lg mr-2 hover:bg-neutral-focus transition duration-300"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="btn btn-primary px-4 py-2 rounded-lg hover:bg-primary-focus transition duration-300"
              >
                Save Changes
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import api from '@/api';
import Swal from 'sweetalert2';

export default {
  props: ['lesson_id', 'module_id'],
  data() {
    return {
      lesson: null, // Lesson data
      loading: true, // Loading state
      error: null, // Error message
      isEditModalOpen: false, // Edit modal state
      editedLesson: {}, // Edited lesson data
      file: null, // Uploaded file
      video: null, // Uploaded video
    };
  },
  async created() {
    try {
      // Fetch lesson data from API
      const response = await api.get(`/app/lessons/?lesson_id=${this.lesson_id}&module_id=${this.module_id}`);
      this.lesson = response.data[0]; // Set the received data
      this.editedLesson = { ...this.lesson }; // Initialize editedLesson with current lesson data
    } catch (err) {
      this.error = 'Failed to fetch lesson data. Please try again.'; // Set error message
      Swal.fire({
        icon: 'error',
        title: 'Error!',
        text: 'Failed to fetch lesson data. Please try again.',
        confirmButtonText: 'OK',
      });
    } finally {
      this.loading = false; // Stop loading
    }
  },
  methods: {
    openEditModal() {
      this.isEditModalOpen = true;
    },
    closeEditModal() {
      if (JSON.stringify(this.editedLesson) !== JSON.stringify(this.lesson) || this.file || this.video) {
        Swal.fire({
          icon: 'warning',
          title: 'Are you sure?',
          text: 'You have unsaved changes. Are you sure you want to close?',
          showCancelButton: true,
          confirmButtonText: 'Yes, close',
          cancelButtonText: 'No, stay',
        }).then((result) => {
          if (result.isConfirmed) {
            this.isEditModalOpen = false;
          }
        });
      } else {
        this.isEditModalOpen = false;
      }
    },
    handleFileUpload(event) {
      this.file = event.target.files[0];
      Swal.fire({
        icon: 'success',
        title: 'File uploaded!',
        text: 'Your file has been uploaded successfully.',
        confirmButtonText: 'OK',
      });
    },
    handleVideoUpload(event) {
      this.video = event.target.files[0];
      Swal.fire({
        icon: 'success',
        title: 'Video uploaded!',
        text: 'Your video has been uploaded successfully.',
        confirmButtonText: 'OK',
      });
    },
    async submitEdit() {
      try {
        const formData = new FormData();

        Object.keys(this.editedLesson).forEach(key => {
          if (this.editedLesson[key] !== this.lesson[key]) {
            formData.append(key, this.editedLesson[key]);
          }
        });

        if (this.file) {
          formData.append('file', this.file);
        }

        if (this.video) {
          formData.append('video', this.video);
        }

        const response = await api.patch(`/app/lessons/update-lesson/?lesson_id=${this.lesson_id}`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        this.lesson = response.data;
        this.closeEditModal();

        Swal.fire({
          icon: 'success',
          title: 'Updated!',
          text: 'The lesson has been updated successfully.',
          confirmButtonText: 'OK',
        });
      } catch (err) {
        this.error = 'Failed to update lesson. Please try again.';
        Swal.fire({
          icon: 'error',
          title: 'Error!',
          text: 'Failed to update lesson. Please try again.',
          confirmButtonText: 'OK',
        });
      }
    },
    confirmDelete() {
      Swal.fire({
        icon: 'warning',
        title: 'Are you sure?',
        text: 'You are about to delete this lesson. This action cannot be undone!',
        showCancelButton: true,
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'No, cancel',
      }).then(async (result) => {
        if (result.isConfirmed) {
          await this.deleteLesson();
        }
      });
    },
    async deleteLesson() {
      try {
        await api.delete(`/app/lessons/delete-lesson/?lesson_id=${this.lesson_id}`);
        Swal.fire({
          icon: 'success',
          title: 'Deleted!',
          text: 'The lesson has been deleted successfully.',
          confirmButtonText: 'OK',
        }).then(() => {
          // Redirect or perform any action after deletion
          this.$router.push({name:'MyModule'}); // Example: Redirect to lessons list
        });
      } catch (err) {
        Swal.fire({
          icon: 'error',
          title: 'Error!',
          text: 'Failed to delete the lesson. Please try again.',
          confirmButtonText: 'OK',
        });
      }
    },
  },
};
</script>

<style scoped>
/* Add any custom styles here */
</style>