<template>
  <main class="bg-base-300 min-h-screen p-4">
    <div class="container mx-auto">
      <h1 class="text-2xl font-bold text-center text-base-content mb-6">
        {{ $t('createCourse.title') }}
      </h1>

      <form
        @submit.prevent="submitForm"
        class="max-w-lg mx-auto bg-base-200 p-6 rounded-lg shadow-md"
      >
        <!-- حقل العنوان -->
        <div class="mb-4">
          <label for="title" class="block text-sm font-medium text-base-content">
            {{ $t('createCourse.courseTitle') }}
          </label>
          <input
            type="text"
            id="title"
            v-model="course.title"
            :placeholder="$t('createCourse.enterCourseTitle')"
            required
            class="mt-1 block w-full px-4 py-2 bg-base-100 border border-base-300 rounded-md text-base-content focus:ring-primary focus:border-primary"
          />
        </div>

        <!-- حقل الوصف -->
        <div class="mb-4">
          <label
            for="description"
            class="block text-sm font-medium text-base-content"
          >
            {{ $t('createCourse.courseDescription') }}
          </label>
          <textarea
            id="description"
            v-model="course.description"
            :placeholder="$t('createCourse.enterCourseDescription')"
            required
            class="mt-1 block w-full px-4 py-2 bg-base-100 border border-base-300 rounded-md text-base-content focus:ring-primary focus:border-primary"
            rows="4"
          ></textarea>
        </div>

        <!-- حقل الصورة -->
        <div class="mb-4">
          <label for="image" class="block text-sm font-medium text-base-content">
            {{ $t('createCourse.courseImage') }}
          </label>
          <input
            type="file"
            id="image"
            @change="handleImageUpload"
            accept="image/*"
            required
            class="mt-1 block w-full text-sm text-base-content file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:bg-primary file:text-base-content hover:file:bg-primary-focus"
          />
          <div v-if="course.imagePreview" class="mt-4">
            <img
              :src="course.imagePreview"
              :alt="$t('createCourse.courseImage')"
              class="w-full h-40 object-cover rounded-md"
            />
          </div>
        </div>

        <!-- حقل هل الدورة مدفوعة؟ -->
        <div class="mb-4">
          <label class="flex items-center">
            <input
              type="checkbox"
              v-model="course.is_paid"
              class="form-checkbox h-5 w-5 text-primary rounded focus:ring-primary"
            />
            <span class="ml-2 text-sm text-base-content">
              {{ $t('createCourse.isPaid') }}
            </span>
          </label>
        </div>

        <!-- حقل السعر (يظهر فقط إذا كانت الدورة مدفوعة) -->
        <div v-if="course.is_paid" class="mb-4">
          <label for="price" class="block text-sm font-medium text-base-content">
            {{ $t('createCourse.coursePrice') }}
          </label>
          <input
            type="number"
            id="price"
            v-model="course.price"
            :placeholder="$t('createCourse.enterCoursePrice')"
            :required="course.is_paid"
            class="mt-1 block w-full px-4 py-2 bg-base-100 border border-base-300 rounded-md text-base-content focus:ring-primary focus:border-primary"
          />
        </div>

        <!-- زر الإرسال -->
        <div>
          <button
            type="submit"
            class="w-full px-4 py-2 btn btn-primary text-base-content rounded-md hover:bg-primary-focus focus:outline-none focus:ring-2 focus:ring-primary"
          >
            {{ $t('createCourse.createCourseButton') }}
          </button>
        </div>
      </form>
    </div>
  </main>
</template>

<script>
import api from "@/api";
import Swal from 'sweetalert2';
export default {
  data() {
    return {
      course: {
        title: "",
        description: "",
        image: null,
        imagePreview: "",
        is_paid: false, //
        price: null,
      },
    };
  },
  methods: {
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.course.image = file;
        this.course.imagePreview = URL.createObjectURL(file);
      }
    },
    async submitForm() {
      try {
        const formData = new FormData();
        formData.append("title", this.course.title);
        formData.append("description", this.course.description);
        formData.append("image", this.course.image);
        formData.append("is_paid", this.course.is_paid);
        formData.append("price", this.course.price ? this.course.price : 0);

        const response = await api.post("/app/courses/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        Swal.fire({
          icon: "success",
          title: "Success!",
          text: "The course has been created successfully.",
        }).then(() => {
          this.$router.push({ name: "Dashboard" });
        });

      } catch (error) {
        if (error.response && error.response.data) {
          console.error("Error response:", error.response.data);
          this.errorMessage =
            error.response.data.detail || "An error occurred.";
        } else {
          console.error("Unexpected error:", error);
          this.errorMessage = "An unexpected error occurred.";
        }
      }
    },
  },
};
</script>
