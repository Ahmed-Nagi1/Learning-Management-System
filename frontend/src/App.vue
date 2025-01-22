<script setup>
import { reactive, provide } from "vue";
import { setLoadingHandler } from "@/api";
import Loading from "./components/Loading.vue";

const state = reactive({
  isLoading: false, // حالة شاشة الانتظار
});

// وظيفة لتغيير حالة شاشة الانتظار
const setLoading = (status) => {
  state.isLoading = status;
};

// ربط شاشة الانتظار مع axios
setLoadingHandler(setLoading);

// توفير الحالة للمكونات الفرعية إذا لزم الأمر
provide("isLoading", state.isLoading);
</script>

<template>
  <div id="app">
    <Loading v-if="state.isLoading" />
    
    <header class="bg-white dark:bg-gray-800 shadow-md"></header>
    <main>
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
</style>
