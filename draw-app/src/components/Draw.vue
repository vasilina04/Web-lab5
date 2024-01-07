<template>
  <div>
    <button @click="showRules" v-if="!gameStarted">Показать правила</button>
  <div v-if="!gameStarted">
    <img alt="logo" src="../assets/img.png">

    <div v-if="rulesVisible" class="popup">
      <h2>Название игры</h2>
      <p>Тут будут правила вашей игры...</p>
    </div>
    <button @click="startGame" v-if="!gameStarted">Начать игру</button>
  </div>
    <div v-if="gameStarted">
      <div>
        <input type="color" v-model="lineColor" />
        <input type="range" min="1" max="20" v-model="lineWidth" />
        <button @click="clearCanvas">Clear</button>
      </div>
      <canvas ref="canvas" :width="1200" :height="1200" @mousedown="startDrawing" @mousemove="draw" @mouseup="endDrawing" @touchstart="startDrawing" @touchmove="draw" @touchend="endDrawing" />
      <div class="canvas-container">
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DrawingCanvas',
  data() {
    return {
      rulesVisible: false,
      gameStarted: false,
      timerId: null,
      timeLimit: 20,
      isDrawing: false,
      context: null,
      lineColor: '#000000', // Цвет по умолчанию
      lineWidth: 5 // Толщина линии по умолчанию
    };
  },
  methods: {
    showRules() {
      this.rulesVisible = true;
    },
    startGame() {
      this.rulesVisible = false;
      this.gameStarted = true;
      this.startTimer();
    },
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
    },
    clearCanvas() {
      const canvas = this.$refs.canvas;
      const context = canvas.getContext('2d');
      context.clearRect(0, 0, canvas.width, canvas.height);
    },
    startTimer() {
      this.timerId = setInterval(() => {
        this.timeLimit--;
        if (this.timeLimit === 0) {
          clearInterval(this.timerId);
          // Код для окончания игры после таймера
        }
      }, 1000);
    },
  }
};
</script>

<style>
@media screen and (max-width: 768px) {
  .popup {
    /* стили для маленьких экранов */
  }

  .show-rules-btn {
    /* стили для кнопки "Показать правила" на маленьких экранах */
  }
}
.popup {
  display: none;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #fff;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}
.canvas-container {
  margin-top: 20px;
  position: relative;
}
canvas {
  border: 1px solid #000;
}

</style>
