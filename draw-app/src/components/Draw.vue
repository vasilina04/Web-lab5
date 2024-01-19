<template>
  <div>
    <button @click="openFullscreenPopup" v-if="!gameStarted && !fullscreenPopupVisible && !drawingSubjectPromptVisible">Правила игры</button>
    <transition name="slide">
    <div v-if="fullscreenPopupVisible" class="fullscreen-popup covercard">
      <h2>Что это за игра?</h2>
      <p class="fullscreen-text">Игра Draw it использует технологии машинного обучения.
        Вы рисуете предмет, а нейронная сеть пытается угадать, что это такое.
        Пока она умеет распознавать лишь немного предметов, но со временем их список расширится.
        Чтобы узнать больше, посмотрите видео ниже.
      </p>
      <div>
      <iframe width="1050" height="595" src="https://www.youtube.com/embed/X8v1GWzZYJ4" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
      </div>
      <button class="close" @click="closeFullscreenPopup">Закрыть</button>
    </div>
  </transition>
  </div>
    <div v-if="gameStarted && !fullscreenPopupVisible && !drawingSubjectPromptVisible" class="canvas-page">
      <div class="canvas-content">
        <div class="timer">
          <p>Оставшееся время: {{ countdownTime }}</p>
        </div>
        <div class="task">
          <p>Нарисуйте этот предмет: {{ selectedDrawingSubject }}</p>
        </div>
        <div class="canvas-btns">
          <input type="color" v-model="lineColor" />
          <input type="range" min="1" max="20" v-model="lineWidth" />
          <button class="b-clear c-btn" @click="clearCanvas">Clear</button>
          <button class="b-exit c-btn" @click="endGame" v-if="gameStarted">Выход</button>
          <button class="b-next c-btn" @click="openNextLevelPrompt">Следующий рисунок</button>
        </div>
      </div>
      <canvas ref="canvas" id="drawingCanvas" resize="true" :width="1000" :height="800" @mousedown="startDrawing" @mousemove="draw" @mouseup="endDrawing" @touchstart="startDrawing" @touchmove="draw" @touchend="endDrawing" />
    </div>
  <div>
    <div class="banner" v-if="!gameStarted && !fullscreenPopupVisible && !drawingSubjectPromptVisible">
    </div>
    <div class="main-content" v-if="!gameStarted && !drawingSubjectPromptVisible && !fullscreenPopupVisible">
      <p>Может ли нейросеть научиться распознавать рисунки?</p>
      <button class="p-button" @click="openPromptForDrawingSubject">Начать игру</button>
    </div>
    <transition name="slide">
    <div v-if="drawingSubjectPromptVisible && !gameStarted && !fullscreenPopupVisible" class="prompt-dialog">
      <button  class="exit" @click="closeDrawingScreen">Закрыть</button>
      <div class="task-content">
        <p>Нарисуйте предмет <b>{{ selectedDrawingSubject }}</b> за 20 секунд</p>
        <button @click="startGame">Хорошо</button>
      </div>
    </div>
    </transition>
  </div>
</template>

<script>
import NeuralNetwork from '@/NeuralNetwork';
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
      lineWidth: 5, // Толщина линии по умолчанию
      fullscreenPopupVisible: false,
      countdownTime: 20,
      timer: null,
      drawingSubjectPromptVisible: false,
      selectedDrawingSubject: '',
      drawingSubjects: ['Дом', 'Дерево', 'Солнце', "Ёж", "Медведь", "Облако"]
    };
  },
  methods: {
     showRules() {
    this.rulesVisible = true;
  },
    openFullscreenPopup() {
      this.fullscreenPopupVisible = true;
      document.documentElement.style.overflow = 'hidden'; // Чтобы предотвратить прокрутку фона
    },
    closeFullscreenPopup() {
      this.fullscreenPopupVisible = false;
      document.documentElement.style.overflow = ''; // Восстановление прокрутки фона
    },
    startGame() {
      this.rulesVisible = false;
      this.gameStarted = true;
      this.drawingSubjectPromptVisible = false;
      if (this.timer) {
        clearInterval(this.timer); // Остановка предыдущего таймера, если есть
      }
      this.countdownTime = 20; // Сброс времени
      this.timer = setInterval(this.countdown, 1000);
    },
    endGame() {
      this.gameStarted = false;
      this.drawingSubjectPromptVisible = false;
      clearInterval(this.timer);
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
        // Передаем изображение на бэкенд, используя модуль NeuralNetwork
        await NeuralNetwork.sendImageToBackend(imageData);
      } catch (error) {
        console.error('Ошибка при отправке изображения на бэкенд', error);
      }
    },
    countdown() {
      if (this.countdownTime > 0) {
        this.countdownTime--;
      } else {
        this.endGame();
        const randomIndex = Math.floor(Math.random() * this.drawingSubjects.length);
        const randomSubject = this.drawingSubjects[randomIndex];
        this.showDrawingPrompt(randomSubject);
      }
    },
    showDrawingPrompt(subject) {
  this.drawingSubjectPromptVisible = true;
  this.selectedDrawingSubject = subject;
  },
    openPromptForDrawingSubject() {
      const randomIndex = Math.floor(Math.random() * this.drawingSubjects.length);
      this.selectedDrawingSubject = this.drawingSubjects[randomIndex];
      this.drawingSubjectPromptVisible = true;
    },
    openNextLevelPrompt() {
      this.endGame();
      const randomIndex = Math.floor(Math.random() * this.drawingSubjects.length);
      const randomSubject = this.drawingSubjects[randomIndex];
      this.showDrawingPrompt(randomSubject);
      this.drawingSubjectPromptVisible = true;
    },
    closeDrawingScreen() {
      this.drawingSubjectPromptVisible = false;
      document.documentElement.style.overflow = ''; // Восстановление прокрутки фона
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
  position: relative;
  user-select: none;
  -webkit-user-drag: none;
  background-color: white;
  overflow-clip-margin: content-box;
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
  aspect-ratio: auto 1024 / 1366;
}

.banner {
  width: 50%;
  height: 50%;
  left: 25%;
  top: 15vh;
  position: absolute;
  background-position: center;
  background-size: contain;
  background-repeat: no-repeat;
  background-image: url("../assets/banner.png");
}

.main-content {
  position: absolute;
  top: 70%;
  left: 35%;
  color: black;
}

button {
  display: inline-block;
  padding: 15px 25px;
  font-size: 24px;
  cursor: pointer;
  text-align: center;
  text-decoration: none;
  outline: none;
  border: none;
  border-radius: 15px;
  box-shadow: 0 9px #999;
}

.p-button {
  color: #fff;
  background-color: #FCD12A;
}

.button-about {
  position: absolute;
  top: 1%;
  left: 1%;
  color: #fff;
  background-color: #FADA5E;
}

button:active {
  box-shadow: 0 5px #666;
  transform: translateY(4px);
}

.fullscreen-popup {
  position: absolute;
  z-index: 100;
  height: 100vh;
  width: 100vw;
  top: 0;
  left: 0;
  background-color: #ffffff;
}

.fullscreen-text {
  margin-left: 25%;
  margin-right: 25%;
  //color: gray;
}

body {
  margin: 0;
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  font-size: 24px
}

html {
  background-color: #d2b48c;
}

.exit {
  position: absolute;
  top: 1%;
  left: 92%;
}

.slide-leave-active {
  transition: all 0.6s cubic-bezier(1.0, 1.0, 1.0, 2.0);
}
.slide-leave-to
{
  transform: translateY(-1000px);
}

.close {
  position: absolute;
  left: 1%;
  top: 1%;
}

.task-content {
  position: absolute;
  top: 40vh;
  left: 40vw;
}

.prompt-dialog {
  position: absolute;
  z-index: 100;
  height: 100vh;
  width: 100vw;
  top: 0;
  left: 0;
  background-color: #ff7bac;
}

.canvas-btns{
  position: absolute;
  top: 1%;
  right: 1%;
}

.timer {
  position: absolute;
  top: 1%;
  left: 40%;
}

.task {
  position: absolute;
  top: 1%;
  left: 1%;
}

.canvas-content {
  margin-top: 0;
  height: 40px;
  justify-content: space-around;
}
</style>
