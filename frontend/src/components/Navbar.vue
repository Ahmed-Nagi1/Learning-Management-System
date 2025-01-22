<template>
  <div class="navbar bg-base-300">
    <div class="flex ml-auto scale-90 z-30">
      <!-- Dropdown for Theme -->
      <ChangeTheme />

      <!-- Dropdown for Language -->
       <ChangeLanguage />
    </div>
  </div>
</template>

<script>
import ChangeTheme from "./ChangeTheme.vue";
import ChangeLanguage from "./ChangeLanguage.vue";
export default {
  name: "Navbar",
  components: {
    ChangeTheme,
    ChangeLanguage,
  },
};
</script>
