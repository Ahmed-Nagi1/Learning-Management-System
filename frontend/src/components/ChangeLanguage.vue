<template>
    <div class="dropdown dropdown-end">
      <label tabindex="0" class="btn">
        <IconLanguage />
      </label>
      <ul
        tabindex="0"
        class="dropdown-content menu bg-base-100 rounded-box w-52 p-2 shadow mt-2"
      >
        <li>
          <a @click="changeLanguage('ar')">{{ $t('settings.arabic') }}</a>
        </li>
        <li>
          <a @click="changeLanguage('en')">{{ $t('settings.english') }}</a>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import IconLanguage from "./icons/IconLanguage.vue";
  import { useI18n } from "vue-i18n";
  
  export default {
    components: {
      IconLanguage,
    },
    setup() {
      const { locale } = useI18n();
  
      const changeLanguage = (lang) => {
        locale.value = lang;
        localStorage.setItem('selectedLanguage', lang); // حفظ اللغة في التخزين المحلي
      };
  
      return {
        changeLanguage,
      };
    },
  };
  </script>
  