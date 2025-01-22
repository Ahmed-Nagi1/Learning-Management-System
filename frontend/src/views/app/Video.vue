<template>
  <div>
    <video ref="video" controls autoplay></video>
  </div>
</template>

<script>
import shaka from 'shaka-player';

export default {
  props: ['videoSrc'],
  mounted() {
    const video = "https://1024terabox.com/s/1zTbMspeb-bVAUHB08qTt0w";
    const player = new shaka.Player(video);

    // تحقق من أن الرابط هو رابط مباشر
    if (this.videoSrc && this.videoSrc.startsWith('http')) {
      player.load(this.videoSrc).then(() => {
        console.log('Video is successfully loaded');
      }).catch((error) => {
        console.error('Error loading video:', error);
      });

      // تسجيل الأحداث (مثل تغيير الجودة)
      player.addEventListener('adaptation', () => {
        console.log('Quality changed:', player.getVariantTracks());
      });
    } else {
      console.error('Invalid video source:', this.videoSrc);
    }
  },
};
</script>