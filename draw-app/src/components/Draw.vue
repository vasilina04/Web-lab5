<template>
  <div class="header">
    <div class="container">
      <div class="header-line">
        <div>
          <button class="close" @click="closeFullscreenPopup" v-if="fullscreenPopupVisible">Закрыть</button>
          <button class="close" @click="closeDrawingScreen"
                  v-if="drawingSubjectPromptVisible && !gameStarted && !fullscreenPopupVisible">Закрыть
          </button>
          <button class="rule-btn" @click="openFullscreenPopup"
                  v-if="!gameStarted && !fullscreenPopupVisible && !drawingSubjectPromptVisible">Правила игры
          </button>
          <div class="canvas-header" v-if="gameStarted">
            <div class="task">
              <p>Нарисуйте этот предмет: {{ selectedDrawingSubject.rus }}</p>
            </div>
            <div class="timer">
              <p>{{ countdownTime }}</p>
            </div>
            <div class="canvas-btns">
              <button class="b-clear c-btn" @click="clearCanvas">Clear</button>
              <button class="b-exit c-btn" @click="endGame" v-if="gameStarted">Выход</button>
              <button class="b-next c-btn" @click="openNextLevelPrompt">Следующий рисунок</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- Страница с правилами -->
  <transition name="slide">
    <div v-if="fullscreenPopupVisible" class="fullscreen-popup covercard">
      <div class="rule-content">
        <h2>Что это за игра?</h2>
        <p class="fullscreen-text">Игра Draw it использует технологии машинного обучения.
          Вы рисуете предмет, а нейронная сеть пытается угадать, что это такое.
          Пока она умеет распознавать лишь немного предметов, но со временем их список расширится.
          Чтобы узнать больше, посмотрите видео ниже.
        </p>
        <div class="about-video">
          <iframe src="https://www.youtube.com/embed/X8v1GWzZYJ4" frameborder="0" allowfullscreen></iframe>
        </div>
      </div>
    </div>
  </transition>
  <!--/Страница с правилами -->
  <div v-if="gameStarted && !fullscreenPopupVisible && !drawingSubjectPromptVisible" class="canvas-container">
    <canvas ref="canvas" id="drawingCanvas" resize="true" :width="800" :height="800" @mousedown="startDrawing"
            @mousemove="draw" @mouseup="endDrawing" @touchstart="startDrawing" @touchmove="draw"
            @touchend="endDrawing"/>
  </div>
  <div id="AI_guess" class="output-message" v-if="backendResponseVisible && !drawingSubjectPromptVisible && gameStarted && !fullscreenPopupVisible">
    <p>{{ backendResponse.rus }}</p>
  </div>
  <!-- Главная страница -->
  <div class="main-content" v-if="!gameStarted && !drawingSubjectPromptVisible && !fullscreenPopupVisible">
    <div class="banner"></div>
    <p>Может ли нейросеть научиться распознавать рисунки?</p>
    <button class="p-button" @click="openPromptForDrawingSubject">Начать игру</button>
  </div>
  <!--/Главная страница -->

  <div v-if="drawingSubjectPromptVisible && !gameStarted && !fullscreenPopupVisible" class="prompt-dialog">
    <!-- Страница с заданием -->
    <div class="card-content">
      <p>Нарисуйте предмет <b>{{ selectedDrawingSubject.rus }}</b> за 20 секунд</p>
      <button @click="startGame">Хорошо</button>
    </div>
  </div>
  <!--/Страница с заданием -->
</template>

<script>

import NeuralNetwork from '@/NeuralNetwork';

class word {
  constructor(eng, rus) {
    this.eng = eng;
    this.rus = rus;
  }
}
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
      selectedDrawingSubject: new word('', ''),
      drawingSubjects: [new word("chair", "стул"),
                        new word("sun", "солнце"),
                        new word("snail", "улитка"),
                        new word("grass", "трава"),
                        new word("smiley_face", "смайлик"),
                        new word('square', 'квадрат'),
                        new word('stairs', 'лестница'),
                        new word('pig', 'свинья'),
                        new word('cow', 'корова'),
                        new word('snowman', 'снеговик'),
                        new word('snowflake', 'снежинка'),
                        new word('submarine', 'подводная лодка'),
                        new word('cloud', 'облако'),
      ],
      backendResponseVisible: false,
      backendResponse: new word('', '')
    };
  },
  methods: {
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
      this.backendResponse = new word('', '');
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
        const response = await NeuralNetwork.sendImageToBackend(imageData);

        this.backendResponseVisible = true;
        this.backendResponse.eng = response;
        this.backendResponse.rus = response;
        for (let i = 0; i < this.drawingSubjects.length; i++) {
          if (this.backendResponse.eng===this.drawingSubjects[i].eng) { this.backendResponse.rus=this.drawingSubjects[i].rus; }
        }


      } catch (error) {
        console.error('Ошибка при отправке изображения на бэкенд', error);
      }
    },
    countdown() {
      if (this.countdownTime > 0) {
        if (this.backendResponse.eng === this.selectedDrawingSubject.eng) {
          document.getElementById("AI_guess").style.backgroundColor = 'green';
          this.backendResponse.eng = '';
          this.backendResponse.rus = '';
          this.openNextLevelPrompt();
        }
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
  height: 40vh;
  width: 70vw;
  background-position: center;
  background-size: contain;
  background-repeat: no-repeat;
  background-image: url("../assets/banner.png");
  margin-top: 10vh;
}

.main-content {
  position: relative;
  color: black;
  display: flex;
  flex-direction: column;
  text-align: center;
  align-items: center;
  justify-content: space-around;
}

.rule-content {
  display: flex;
  flex-direction: column;
  text-align: center;
  align-items: center;
  padding: 5px 40px;
  width: 100%;
  max-width: 910px;
  justify-content: space-between;
  margin: 0 auto;
}

.about-video {
  position: relative;
  width: 100%;
  height: 0;
  padding-bottom: 56%;
  margin-top: 30px;
  margin-bottom: 30px;
}

iframe {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
}

button {
  display: inline-block;
  padding: 10px 20px;
  font-size: 24px;
  cursor: pointer;
  text-align: center;
  text-decoration: none;
  outline: none;
  border: none;
  border-radius: 12px;
  box-shadow: 0 9px #999;
}

.p-button {
  color: #fff;
  background-color: #FCD12A;
}

button:active {
  box-shadow: 0 5px #666;
  transform: translateY(4px);
}

.fullscreen-popup {
  background-color: #FCD12A;
}

body {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  font-size: 24px
}

.slide-leave-active {
  transition: all 0.6s cubic-bezier(1.0, 1.0, 1.0, 2.0);
}

.slide-leave-to {
  transform: translateY(-1000px);
}

.close {
  color: #fff;
  background-color: #FADA5E;
}

.c-btn {
  color: #fff;
  background-color: #FADA5E;
  margin-right: 10px;
}

.prompt-dialog {
  z-index: 999;
  position: relative;
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

body {
  margin: 0;
  overflow-y: hidden;
  overflow-x: hidden;
}

.card-content {
  position: absolute;
  padding-bottom: 20vh;
}

.timer {
  display: inline-block;
}

.header {
  position: relative;
  background-color: #FCD12A;
  width: 100%;
  padding: 10px 14px;
}

.container {
  margin: 0 20px;
}

.header-line {
  position: relative;
  padding-bottom: 10px;
  display: flex;
  align-items: center;
  text-align: center;
}

.rule-btn {
  color: #fff;
  background-color: #FADA5E;
}

.canvas-header {
  display: flex;
  align-items: center;
  justify-content: space-around;
  width: 100vw;
  left: 0;
}

.output-message {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 5px;
  text-align: center;
}
</style>
