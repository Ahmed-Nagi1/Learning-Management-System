<template>
  <div class="p-8">
    <div class="flex flex-col items-center space-y-6">
      <!-- User Image Display -->
      <div class="avatar relative">
        <div class="w-48 h-48 rounded-full overflow-hidden">
          <img
            :src="user.image || defaultImage"
            alt="User Image"
            class="rounded-full"
            v-if="user.image || defaultImage"
          />
        </div>
        <button
          @click="openFileInput"
          class="btn btn-circle btn-sm absolute bottom-0 right-0"
        >
          <i class="fas fa-pencil-alt"></i>
        </button>
      </div>

      <!-- User Name Input -->
      <div class="form-control w-full max-w-xs">
        <label class="label">
          <span class="label-text text-lg">Full Name</span>
        </label>
        <input
          v-model="user.name"
          type="text"
          placeholder="Full Name"
          class="input input-bordered input-lg w-full"
          :disabled="!isEditingName"
        />
        <button @click="toggleEditName" class="btn btn-sm mt-4 text-lg">
          {{ isEditingName ? 'Save Name' : 'Edit Name' }}
        </button>
      </div>

      <!-- Save Button -->
      <button @click="saveChanges" class="btn btn-primary btn-lg">
        Save Changes
      </button>
    </div>

    <!-- Hidden File Input for Image Upload -->
    <input
      type="file"
      ref="fileInput"
      class="hidden"
      @change="handleImageUpload"
    />
  </div>
</template>

<script>
import api from '@/api';
import Swal from 'sweetalert2'; // استيراد SweetAlert2

export default {
  data() {
    return {
      user: {
        name: "",
        image: "",
      },
      defaultImage: "https://placehold.co/600x400",
      isEditingName: false,
    };
  },
  async created() {
    await this.fetchUserData();
  },
  methods: {
    async fetchUserData() {
      try {
        const response = await api.get("/auth/user-info/");
        this.user.name = response.data.name;
        this.user.image = response.data.image || this.defaultImage;
      } catch (error) {
      }
    },
    openFileInput() {
      this.$refs.fileInput.click();
    },
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.user.image = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    toggleEditName() {
      this.isEditingName = !this.isEditingName;
    },
    async saveChanges() {
      try {
        const formData = new FormData();
        if (this.isEditingName) {
          formData.append("full_name", this.user.name);
        }
        if (this.$refs.fileInput.files[0]) {
          formData.append("profile_image", this.$refs.fileInput.files[0]);
        }

        const response = await api.patch("/auth/user-info/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });

        if (response.status === 200) {
          Swal.fire({
            icon: 'success',
            title: 'Success!',
            text: 'Changes saved successfully!',
            confirmButtonText: 'OK'
          });
          this.isEditingName = false;
        }
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'Failed to save changes!',
          confirmButtonText: 'OK'
        });
      }
    },
  },
};
</script>