<template>
  <main class="bg-base-300 min-h-screen flex items-center justify-center p-6">
    <div class="w-full max-w-4xl">
      <!-- زر العودة -->
      <router-link
        to="/dashboard"
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
        العودة إلى لوحة التحكم
      </router-link>

      <!-- تفاصيل الكورس -->
      <div class="bg-base-200 rounded-lg shadow-lg overflow-hidden p-6">
        <h1 class="text-3xl font-bold text-base-content mb-6">تعديل الكورس</h1>

        <!-- نموذج التعديل -->
        <form @submit.prevent="submitForm" class="space-y-6">
          <!-- حقل العنوان -->
          <div>
            <label for="title" class="block text-sm font-medium text-base-content mb-2">عنوان الكورس</label>
            <input
              type="text"
              id="title"
              v-model="course.title"
              placeholder="أدخل عنوان الكورس"
              required
              class="w-full px-4 py-2 bg-base-100 border border-base-300 rounded-md text-base-content focus:ring-primary focus:border-primary"
            />
          </div>

          <!-- حقل الوصف -->
          <div>
            <label for="description" class="block text-sm font-medium text-base-content mb-2">وصف الكورس</label>
            <textarea
              id="description"
              v-model="course.description"
              placeholder="أدخل وصف الكورس"
              required
              class="w-full px-4 py-2 bg-base-100 border border-base-300 rounded-md text-base-content focus:ring-primary focus:border-primary"
              rows="4"
            ></textarea>
          </div>

          <!-- حقل الصورة -->
          <div>
            <label for="image" class="block text-sm font-medium text-base-content mb-2">صورة الكورس</label>
            <input
              type="file"
              id="image"
              @change="handleImageUpload"
              accept="image/*"
              class="w-full text-sm text-base-content file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:bg-primary file:text-base-content hover:file:bg-primary-focus"
            />
            <div v-if="course.imagePreview" class="mt-4">
              <img :src="course.imagePreview" alt="صورة الكورس" class="w-full h-48 object-cover rounded-md" />
            </div>
          </div>

          <!-- حقل السعر -->
          <div>
            <label for="price" class="block text-sm font-medium text-base-content mb-2">سعر الكورس</label>
            <input
              type="number"
              id="price"
              v-model="course.price"
              placeholder="أدخل سعر الكورس"
              required
              class="w-full px-4 py-2 bg-base-100 border border-base-300 rounded-md text-base-content focus:ring-primary focus:border-primary"
            />
          </div>

          <!-- حقل حالة النشر -->
          <div>
            <label class="flex items-center">
              <input
                type="checkbox"
                v-model="course.is_published"
                class="form-checkbox h-5 w-5 text-primary rounded focus:ring-primary"
              />
              <span class="ml-2 text-sm text-base-content">نشر الكورس</span>
            </label>
          </div>

          <!-- أزرار الإجراءات -->
          <div class="flex justify-end space-x-4">
            <button
              type="button"
              @click="cancelEdit"
              class="px-6 py-2 btn btn-neutral text-base-content rounded-lg hover:bg-neutral-focus focus:outline-none"
            >
              إلغاء
            </button>
            <button
              type="submit"
              class="px-6 py-2 btn btn-primary text-base-content rounded-lg hover:bg-primary-focus focus:outline-none"
            >
              حفظ التعديلات
            </button>
          </div>
        </form>
      </div>
    </div>
  </main>
</template>
<script>
export default {
  data() {
    return {
      course: {
        id: 1,
        title: "دورة Vue.js",
        description:
          "تعلم Vue.js من الصفر إلى الاحتراف. هذه الدورة تغطي كل ما تحتاجه لبناء تطبيقات ويب تفاعلية باستخدام Vue.js.",
        image: "https://via.placeholder.com/800x400",
        imagePreview: "https://via.placeholder.com/800x400",
        price: 200,
        is_published: true,
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
    submitForm() {
      // هنا يمكنك إضافة الكود لحفظ التعديلات
      alert("تم حفظ التعديلات بنجاح!");
    },
    cancelEdit() {
      // هنا يمكنك إضافة الكود للعودة إلى الصفحة السابقة
      this.$router.push("/dashboard");
    },
  },
};
</script>

