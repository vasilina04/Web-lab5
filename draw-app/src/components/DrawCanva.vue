<template>
  <div>
    <div>
      <input type="color" v-model="lineColor" />
      <input type="range" min="1" max="20" v-model="lineWidth" />
      <button @click="clearCanvas">Clear</button>
    </div>
    <canvas ref="canvas" :width="800" :height="600" @mousedown="startDrawing" @mousemove="draw" @mouseup="endDrawing" @touchstart="startDrawing" @touchmove="draw" @touchend="endDrawing" />
  </div>
</template>

<script>
export default {
  name: 'DrawingCanvas',
  data() {
    return {
      isDrawing: false,
      context: null,
      lineColor: '#000000',
      lineWidth: 5,
    };
  },
  methods: {
    startDrawing(event) {
      this.isDrawing = true;
      const canvas = this.$refs.canvas;
      this.context = canvas.getContext('2d');
      this.context.lineWidth = this.lineWidth;
      this.context.strokeStyle = this.lineColor;
      const x = event.type === 'touchstart' ? event.touches[0].clientX - canvas.offsetLeft : event.offsetX;
      const y = event.type === 'touchstart' ? event.touches[0].clientY - canvas.offsetTop : event.offsetY;
      this.context.beginPath();
      this.context.moveTo(x, y);
    },
    draw(event) {
      if (this.isDrawing) {
        const canvas = this.$refs.canvas;
        const x = event.type === 'touchmove' ? event.touches[0].clientX - canvas.offsetLeft : event.offsetX;
        const y = event.type === 'touchmove' ? event.touches[0].clientY - canvas.offsetTop : event.offsetY;
        this.context.lineTo(x, y);
        this.context.stroke();
      }
    },
    endDrawing() {
      this.isDrawing = false;
      this.sendImageToBackend();
    },
    clearCanvas() {
      const canvas = this.$refs.canvas;
      const context = canvas.getContext('2d');
      context.clearRect(0, 0, canvas.width, canvas.height);
    },
    async sendImageToBackend() {
      const imageData = this.$refs.canvas.toDataURL('image/png');

      try {
        const response = await this.$axios.post('http://localhost:8000/inbetweener/api/analyze/', { image: imageData });
        console.log(response.data); // Обработка ответа от бэкенда
      } catch (error) {
        console.error('Ошибка при отправке изображения на бэкенд', error);
      }
    },
  },
};
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
