<template>
    <div class="navbar bg-base-300">
      <div class="flex gap-x-4 ml-auto">
        <!-- Dropdown for Theme -->
        <div class="dropdown dropdown-end">
          <label tabindex="0" class="btn">
            <IconTheme />
          </label>
          <ul
            tabindex="0"
            class="dropdown-content menu bg-base-100 rounded-box w-52 p-2 shadow mt-2"
          >
            <!-- عرض الثيمات كخيارات -->
            <li v-for="theme in themes" :key="theme">
              <a @click="changeTheme(theme)">{{ theme }}</a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import IconLanguage from "./icons/IconLanguage.vue";
  import IconTheme from "./icons/IconTheme.vue";
  
  export default {
    components: {
      IconLanguage,
      IconTheme,
    },
    data() {
      return {
        themes: ["dark", "light", "night", "cupcake"], 
      };
    },
    mounted() {
      const savedTheme = localStorage.getItem("theme");
      if (savedTheme) {
        this.changeTheme(savedTheme);
      }
    },
    methods: {
      changeTheme(theme) {
        // تغيير الثيم
        document.documentElement.setAttribute("data-theme", theme);
  
        // حفظ الثيم في localStorage
        localStorage.setItem("theme", theme);
      },
    },
  };
  </script>