<template>
  <div class="p-4 sm:p-6">
    <h1 class="text-2xl font-bold mb-6">{{ $t("studentsTable.title") }}</h1>

    <!-- جدول الطلاب -->
    <div class="overflow-x-auto bg-base-200 rounded-lg shadow-lg">
      <table class="table w-full">
        <!-- رأس الجدول -->
        <thead>
          <tr>
            <th class="text-left p-4">{{ $t("studentsTable.name") }}</th>
            <th class="text-left p-4">{{ $t("studentsTable.email") }}</th>
          </tr>
        </thead>
        <!-- جسم الجدول -->
        <tbody>
          <tr
            v-for="student in students"
            :key="student.id"
            class="hover:bg-base-100 transition-colors"
          >
            <td class="p-4">{{ student.name }}</td>
            <td class="p-4">{{ student.email }}</td>
            <td class="p-4">
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- حالة التحميل -->
    <div v-if="isLoading" class="mt-6 text-center">
      <span class="loading loading-spinner text-primary"></span>
      <p>{{ $t("studentsTable.loading") }}</p>
    </div>

    <!-- رسالة الخطأ -->
    <div v-if="error" class="mt-6 text-center text-error">
      <p>{{ $t("studentsTable.error") }}: {{ error }}</p>
    </div>
  </div>
</template>

<script>
import api from "@/api";
import Swal from "sweetalert2";

export default {
  name: "StudentsTable",
  props: ["id"],
  data() {
    return {
      students: [], 
      isLoading: true, 
      error: null, 
    };
  },
  async created() {
    try {
      const response = await api.get(`/app/enrollment/get-my-students/?course=${this.id}`);
      if (response.status===200) {
        
        this.students = response.data.map(student => ({
          id: student.student__email,
          name: student.student__full_name,
          email: student.student__email,
        }));
      }
    } catch (err) {
      this.error = err.message || this.$t("studentsTable.defaultError");
    } finally {
      this.isLoading = false;
    }
  },
  methods: {
    // تأكيد الحذف
    confirmDelete(studentId) {
      Swal.fire({
        title: this.$t("studentsTable.deleteConfirmationTitle"),
        text: this.$t("studentsTable.deleteConfirmationText"),
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: this.$t("studentsTable.delete"),
        cancelButtonText: this.$t("studentsTable.cancel"),
      }).then((result) => {
        if (result.isConfirmed) {
          this.deleteStudent(studentId);
        }
      });
    },

  },
};
</script>

<style scoped>
.table th,
.table td {
  padding: 1rem;
}
</style>