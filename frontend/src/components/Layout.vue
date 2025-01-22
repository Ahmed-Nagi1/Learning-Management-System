<template>
    <div>
        <Sidebar />
      <Navbar />
      <router-view />
    </div>
  </template>
  
  <script>
  import Sidebar from './Sidebar.vue';
  import Navbar from './Navbar.vue';
  
  export default {
    components: {
      Sidebar,
      Navbar,
    },
  };
  </script>
  