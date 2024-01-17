import axios from 'axios';

const NeuralNetwork = {
  async sendImageToBackend(imageData) {
    try {
      // Передаем изображение и модель на бэкенд для обработки
      console.log(imageData);
      const response = await axios.post('http://localhost:8000/inbetweener/api/analyze/', { image: imageData });
      console.log(response.data); // Обработка ответа от бэкенда
    } catch (error) {
      console.error('Ошибка при отправке изображения на бэкенд', error);
    }
  },
};

export default NeuralNetwork;
