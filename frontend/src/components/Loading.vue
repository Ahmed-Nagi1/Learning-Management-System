<template>
  <div v-if="isVisible" class="flex items-center justify-center fixed inset-0 bg-black bg-opacity-50 z-50">
    <div class="hourglass relative w-12 h-20 bg-gradient-to-b from-blue-500 via-gray-400 to-blue-500 clip-path-hourglass animate-flip">
      <div class="absolute top-1 left-1 w-10 h-16 bg-gray-800 clip-path-fill animate-fill"></div>
      <div class="absolute top-0 left-0 w-full h-full bg-gradient-to-r from-transparent via-gray-300 to-transparent opacity-30 animate-glare"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Hourglass",
  props: {
    isVisible: {
      type: Boolean,
      default: true, 
    },
  },
};
</script>

<style scoped>
@keyframes fill {
  from {
    clip-path: polygon(
      0% 0%,
      100% 0%,
      100% 24%,
      50% 47%,
      50% 47%,
      50% 47%,
      50% 47%,
      50% 47%,
      50% 47%,
      50% 47%,
      50% 47%,
      0% 24%
    );
  }
  10% {
    clip-path: polygon(
      0% 4%,
      100% 4%,
      100% 24%,
      55% 45%,
      55% 100%,
      55% 100%,
      55% 100%,
      45% 100%,
      45% 100%,
      45% 100%,
      45% 45%,
      0% 24%
    );
  }
  45% {
    clip-path: polygon(
      0% 24%,
      100% 24%,
      100% 24%,
      55% 45%,
      55% 80%,
      100% 100%,
      100% 100%,
      0% 100%,
      0% 100%,
      45% 80%,
      45% 45%,
      0% 24%
    );
  }
  80% {
    clip-path: polygon(
      45% 45%,
      55% 45%,
      55% 45%,
      55% 45%,
      55% 58%,
      100% 76%,
      100% 100%,
      0% 100%,
      0% 76%,
      45% 58%,
      45% 45%,
      45% 45%
    );
  }
  85%,
  to {
    clip-path: polygon(
      50% 53%,
      50% 53%,
      50% 53%,
      50% 53%,
      50% 53%,
      100% 76%,
      100% 100%,
      0% 100%,
      0% 76%,
      50% 53%,
      50% 53%,
      50% 53%
    );
  }
}
@keyframes glare {
  from,
  90% {
    transform: translateX(0);
  }
  to {
    transform: translateX(3em);
  }
}
@keyframes flip {
  from,
  90% {
    transform: rotate(0);
  }
  to {
    transform: rotate(180deg);
  }
}

.clip-path-hourglass {
  clip-path: polygon(
    0% 0%,
    100% 0%,
    100% 5.55%,
    95% 5.55%,
    95% 28%,
    60% 46%,
    60% 54%,
    95% 72%,
    95% 94.45%,
    100% 94.45%,
    100% 100%,
    0% 100%,
    0% 94.45%,
    5% 94.45%,
    5% 72%,
    40% 54%,
    40% 46%,
    5% 28%,
    5% 5.55%,
    0% 5.55%
  );
}
.clip-path-fill {
  clip-path: polygon(
    0% 0%,
    100% 0%,
    100% 24%,
    50% 47%,
    50% 47%,
    50% 47%,
    50% 47%,
    50% 47%,
    50% 47%,
    50% 47%,
    50% 47%,
    0% 24%
  );
}
.animate-flip {
  animation: flip 2s ease-in-out infinite;
}
.animate-fill {
  animation: fill 2s linear infinite;
}
.animate-glare {
  animation: glare 2s linear infinite;
}
</style>