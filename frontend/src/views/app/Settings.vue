<template>
  <main class="bg-base-100 dark:bg-base-300 min-h-screen p-4 sm:p-6">
    <div class="container mx-auto">
      <h1 class="text-2xl sm:text-3xl font-bold text-center text-base-content dark:text-base-content mb-6 sm:mb-8">
        {{ t('settings.title') }}
      </h1>
      <div class="bg-base-200 dark:bg-base-200 rounded-lg shadow-lg p-6 max-w-2xl mx-auto">
  
        <!-- قسم اللغة -->
        <div class="mb-6">
          <h2 class="text-lg sm:text-xl font-bold text-base-content dark:text-base-content mb-2">
            {{ t('settings.language') }}
          </h2>
          <select
            v-model="language"
            @change="changeLanguage"
            class="w-full p-2 border rounded-lg bg-base-100 text-base-content dark:bg-base-100 dark:text-base-content"
          >
            <option value="en">{{ t('settings.english') }}</option>
            <option value="ar">{{ t('settings.arabic') }}</option>
          </select>
        </div>
  
        <!-- قسم البريد الإلكتروني -->
        <div class="mb-6">
          <h2 class="text-lg sm:text-xl font-bold text-base-content dark:text-base-content mb-2">
            {{ t('settings.info') }}
          </h2>
          <button
            @click="router.push({ name: 'Info' })"
            class="btn btn-primary w-full"
          >
            {{ t('settings.info') }}
          </button>
        </div>
  
        <!-- قسم البريد الإلكتروني -->
        <div class="mb-6">
          <h2 class="text-lg sm:text-xl font-bold text-base-content dark:text-base-content mb-2">
            {{ t('settings.email') }}
          </h2>
          <button
            @click="router.push({ name: 'changeEmail' })"
            class="btn btn-primary w-full"
          >
            {{ t('settings.changeEmail') }}
          </button>
        </div>
  
        <!-- قسم كلمة المرور -->
        <div class="mb-6">
          <h2 class="text-lg sm:text-xl font-bold text-base-content dark:text-base-content mb-2">
            {{ t('settings.password') }}
          </h2>
          <button
            @click="router.push({ name: 'changePassword' })"
            class="btn btn-primary w-full"
          >
            {{ t('settings.changePassword') }}
          </button>
        </div>

        <!-- زر تسجيل الخروج -->
        <div class="mt-8">
          <button
            @click="logout"
            class="w-full btn btn-error text-white py-2 px-4 rounded-lg hover:bg-error-focus transition duration-300"
          >
            {{ t('settings.logout') }}
          </button>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import Swal from 'sweetalert2';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const { t, locale } = useI18n(); // استخدام Composition API
    const router = useRouter();
    const language = ref(locale.value); // اللغة الحالية

    const changeLanguage = () => {
      locale.value = language.value; // تغيير اللغة
    };

    const logout = () => {
      Swal.fire({
        title: t('settings.logoutConfirmTitle'),
        text: t('settings.logoutConfirmText'),
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: t('settings.logoutConfirmButton'),
        cancelButtonText: t('settings.logoutCancelButton'),
      }).then((result) => {
        if (result.isConfirmed) {
          localStorage.clear();
          router.push({ name: 'login' });
        }
      });
    };

    return {
      t,
      language,
      changeLanguage,
      logout,
      router,
    };
  },
};
</script>