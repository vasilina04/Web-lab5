<template>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css" rel="stylesheet" type="text/css">
  <div>
    <button class = "button-about" @click="openFullscreenPopup" v-if="!gameStarted && !fullscreenPopupVisible && !drawingSubjectPromptVisible">Правила</button>
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
    <div v-if="gameStarted && !fullscreenPopupVisible && !drawingSubjectPromptVisible">
      <div>
        <p>Оставшееся время: {{ countdownTime }}</p>
         <p>Нарисуйте предмет {{ selectedDrawingSubject }}</p>
        <input type="color" v-model="lineColor" />
        <input type="range" min="1" max="20" v-model="lineWidth" />
        <button class="b-clear c-btn" @click="clearCanvas">Clear</button>
        <button class="b-exit c-btn" @click="endGame" v-if="gameStarted">Выход</button>
        <button class="b-next c-btn" @click="openNextLevelPrompt">Следующий рисунок</button>
      </div>
      <canvas ref="canvas" :width="800" :height="800" @mousedown="startDrawing" @mousemove="draw" @mouseup="endDrawing" @touchstart="startDrawing" @touchmove="draw" @touchend="endDrawing" />
    </div>
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
        <p>Нарисуйте {{ selectedDrawingSubject }} за 20 секунд</p>
        <button @click="startGame">Хорошо</button>
      </div>
    </div>
    </transition>


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
    },
    clearCanvas() {
      const canvas = this.$refs.canvas;
      const context = canvas.getContext('2d');
      context.clearRect(0, 0, canvas.width, canvas.height);
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
  border: 1px solid #000;
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
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  font-size: 24px;
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
  background-color: #ffffff;
}

.c-btn {
  position: relative;
  top: -1.2vh;
}

</style>
