<template>
  <main
    class="bg-base-300 min-h-screen flex items-center justify-center p-4 sm:p-6"
  >
    <div class="w-full max-w-4xl">
      <!-- Back to Dashboard Link -->
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
        {{ $t("infoCourse.backToDashboard") }}
      </router-link>

      <!-- Course Details -->
      <div class="bg-base-200 rounded-lg shadow-lg overflow-hidden">
        <!-- Course Image -->
        <img
          :src="course.image"
          :alt="course.title"
          class="w-full h-48 sm:h-64 object-cover cursor-pointer"
          @click="showLightbox"
        />

        <!-- Course Content -->
        <div class="p-4 sm:p-6 text-center">
          <h1 class="text-2xl sm:text-3xl font-bold text-base-content mb-4">
            {{ course.title }}
          </h1>

          <!-- Additional Information -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6 mb-6">
            <!-- Price -->
            <div>
              <h2 class="text-lg sm:text-xl font-bold text-base-content mb-2">
                {{ $t("infoCourse.price") }}
              </h2>
              <p
                class="text-base sm:text-lg"
                :class="course.is_paid ? 'text-primary' : 'text-success'"
              >
                {{
                  course.is_paid ? `SAR ${course.price}` : $t("infoCourse.free")
                }}
              </p>
            </div>

            <!-- Number of Students -->
            <div>
              <h2 class="text-lg sm:text-xl font-bold text-base-content mb-2">
                {{ $t("infoCourse.students") }}
              </h2>
              <p class="text-base sm:text-lg text-base-content">
                {{ course.students_in_course }}
              </p>
            </div>

            <!-- Rating -->
            <div>
              <h2 class="text-lg sm:text-xl font-bold text-base-content mb-2">
                {{ $t("infoCourse.rating") }}
              </h2>
              <p class="text-base sm:text-lg text-warning">
                {{ course.rating }} / 5
              </p>
            </div>

            <!-- Status -->
            <div>
              <h2 class="text-lg sm:text-xl font-bold text-base-content mb-2">
                {{ $t("infoCourse.status") }}
              </h2>
              <p class="text-base sm:text-lg text-base-content">
                {{
                  course.is_published
                    ? $t("infoCourse.published")
                    : $t("infoCourse.unpublished")
                }}
              </p>
            </div>
          </div>

          <!-- Detailed Description -->
          <div class="mt-6 text-left">
            <h2 class="text-lg sm:text-xl font-bold text-base-content mb-2">
              {{ $t("infoCourse.description") }}
            </h2>
            <div
              class="text-base-content text-base sm:text-lg bg-base-100 p-4 rounded-lg"
            >
              {{ course.description || $t("infoCourse.noDescription") }}
            </div>
          </div>

          <!-- Actions -->
          <div
            class="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-4 mt-6"
          >
            <button
              @click="openEditModal"
              class="px-6 py-2 btn btn-primary text-base-content rounded-lg hover:bg-primary-focus focus:outline-none"
            >
              {{ $t("infoCourse.editCourse") }}
            </button>
            <button
              @click="confirmDelete"
              class="px-6 py-2 btn btn-error text-base-content rounded-lg hover:bg-error-focus focus:outline-none"
            >
              {{ $t("infoCourse.deleteCourse") }}
            </button>
            <router-link
              :to="{ name: 'MyModule', params: { id: id } }"
              class="px-6 py-2 btn btn-success text-base-content rounded-lg hover:bg-success-focus focus:outline-none"
            >
              {{ $t("infoCourse.viewChapters") }}
            </router-link>
            <!-- Add Student Button -->
            <button
              v-if="course.is_paid"
              @click="openAddStudentModal"
              class="px-6 py-2 btn btn-info text-base-content rounded-lg hover:bg-info-focus focus:outline-none"
            >
              {{ $t("infoCourse.addStudent") }}
            </button>
            <!-- Get All Student Button -->
            <router-link
              :to="{ name: 'StudentsList', params: { id: id } }"
              class="px-6 py-2 bg-yellow-400 text-black rounded-lg hover:bg-yellow-500 focus:outline-none"
            >
            <p></p>
            {{ $t("infoCourse.getStudents") }}
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div
      v-if="isEditModalOpen"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4"
    >
      <div class="bg-base-200 rounded-lg shadow-lg w-full max-w-2xl p-4 sm:p-6">
        <h2 class="text-xl sm:text-2xl font-bold text-base-content mb-6">
          {{ $t("infoCourse.editCourse") }}
        </h2>
        <!-- Edit Fields -->
        <div class="space-y-4">
          <div>
            <label class="block text-base-content mb-2">{{
              $t("infoCourse.courseName")
            }}</label>
            <input
              v-model="editedCourse.title"
              type="text"
              class="w-full bg-base-100 text-base-content rounded-lg p-2"
            />
          </div>
          <div>
            <label class="block text-base-content mb-2">{{
              $t("infoCourse.courseImage")
            }}</label>
            <input
              type="file"
              @change="handleImageUpload"
              class="w-full bg-base-100 text-base-content rounded-lg p-2"
            />
            <img
              v-if="editedCourse.imagePreview"
              :src="editedCourse.imagePreview"
              alt="Image Preview"
              class="mt-2 w-32 h-32 object-cover rounded-lg"
            />
          </div>
          <div>
            <label class="block text-base-content mb-2">{{
              $t("infoCourse.description")
            }}</label>
            <textarea
              v-model="editedCourse.description"
              class="w-full bg-base-100 text-base-content rounded-lg p-2"
            ></textarea>
          </div>
          <div>
            <label class="block text-base-content mb-2">{{
              $t("infoCourse.isPaid")
            }}</label>
            <input
              type="checkbox"
              v-model="editedCourse.is_paid"
              class="text-base-content bg-primary rounded-lg p-2"
            />
          </div>
          <div v-if="editedCourse.is_paid">
            <label class="block text-base-content mb-2">{{
              $t("infoCourse.price")
            }}</label>
            <input
              v-model="editedCourse.price"
              type="number"
              class="w-full bg-base-100 text-base-content rounded-lg p-2"
            />
          </div>
        </div>
        <!-- Edit Buttons -->
        <div class="flex justify-end space-x-4 mt-6">
          <button
            @click="closeEditModal"
            class="px-6 py-2 btn btn-neutral text-base-content rounded-lg hover:bg-neutral-focus focus:outline-none"
          >
            {{ $t("infoCourse.cancel") }}
          </button>
          <button
            @click="updateCourse"
            class="px-6 py-2 btn btn-primary text-base-content rounded-lg hover:bg-primary-focus focus:outline-none"
          >
            {{ $t("infoCourse.saveChanges") }}
          </button>
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
import api from "@/api";
import Swal from "sweetalert2";
import VueEasyLightbox from "vue-easy-lightbox";

export default {
  components: {
    VueEasyLightbox,
  },
  props: ["id"],
  data() {
    return {
      course: {},
      isEditModalOpen: false,
      editedCourse: {
        title: "",
        description: "",
        price: 0,
        is_paid: false,
        image: "",
        imagePreview: "",
        imageFile: null,
      },
      visible: false, // Lightbox visibility
      imgs: [], // Images for Lightbox
      index: 0, // Current image index
    };
  },
  methods: {
    async fetchCourse() {
      try {
        const response = await api.get(`/app/courses/${this.id}`);
        this.course = response.data;
        this.editedCourse = {
          ...response.data,
          imagePreview: response.data.image,
          imageFile: null,
        };
      } catch (e) {
        console.error("An error occurred while fetching courses:", e);
      }
    },
    async deleteCourse() {
      try {
        await api.delete(`/app/courses/${this.$route.params.id}`);
        Swal.fire({
          icon: "success",
          title: "Deleted!",
          text: "The course has been deleted successfully.",
        }).then(() => {
          this.$router.push({ name: "Dashboard" });
        });
      } catch (e) {
        console.error("An error occurred while deleting the course:", e);
        Swal.fire({
          icon: "error",
          title: "Error!",
          text: "An error occurred while trying to delete the course.",
        });
      }
    },
    confirmDelete() {
      Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Yes, delete it!",
        cancelButtonText: "Cancel",
      }).then((result) => {
        if (result.isConfirmed) {
          this.deleteCourse();
        }
      });
    },
    openEditModal() {
      this.isEditModalOpen = true;
    },
    closeEditModal() {
      this.isEditModalOpen = false;
      this.editedCourse.imageFile = null;
      this.editedCourse.imagePreview = this.course.image;
    },
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.editedCourse.imageFile = file;
        this.editedCourse.imagePreview = URL.createObjectURL(file);
      }
    },
    async updateCourse() {
      try {
        const formData = new FormData();
        formData.append("title", this.editedCourse.title);
        formData.append("description", this.editedCourse.description);
        formData.append("is_paid", this.editedCourse.is_paid);

        if (this.editedCourse.is_paid) {
          formData.append("price", this.editedCourse.price);
        }

        if (this.editedCourse.imageFile) {
          formData.append("image", this.editedCourse.imageFile);
        }

        const response = await api.patch(
          `/app/courses/${this.$route.params.id}/`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );

        this.course = response.data;
        this.closeEditModal();
        Swal.fire({
          icon: "success",
          title: "Updated!",
          text: "The course has been updated successfully.",
        });
      } catch (e) {
        console.error("An error occurred while updating the course:", e);
        Swal.fire({
          icon: "error",
          title: "Error!",
          text: "An error occurred while trying to update the course.",
        });
      }
    },
    showLightbox() {
      this.imgs = [this.course.image]; // Set the image for Lightbox
      this.visible = true; // Show Lightbox
    },
    handleHide() {
      this.visible = false; // Hide Lightbox
    },
    // Add Student Methods
    openAddStudentModal() {
      Swal.fire({
        title: "Add Student",
        html: '<input type="email" id="swal-input1" class="swal2-input" placeholder="Student Email">',
        focusConfirm: false,
        preConfirm: () => {
          const studentEmail = Swal.getPopup()
            .querySelector("#swal-input1")
            .value.trim();
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Regular expression to validate email
          if (!studentEmail) {
            Swal.showValidationMessage("Please enter student email");
            return false;
          } else if (!emailRegex.test(studentEmail)) {
            Swal.showValidationMessage("Please enter a valid email address");
            return false;
          }
          return { studentEmail };
        },
      }).then((result) => {
        if (result.isConfirmed) {
          this.addStudent(result.value.studentEmail);
        }
      });
    },

    async addStudent(studentEmail) {
      try {
        const response = await api.post(`/app/enrollment/private-enrollment/`, {
          course: this.id,
          student_email: studentEmail,
        });
        console.log(response.data);
        Swal.fire({
          icon: "success",
          title: "Success!",
          text: response.data.detail,
        });
        this.fetchCourse(); // Refresh course data
      } catch (e) {
        Swal.fire({
          icon: "error",
          title: "Error!",
          text: e.response.data.detail,
        });
      }
    },
  },
  mounted() {
    this.fetchCourse();
  },
};
</script>
