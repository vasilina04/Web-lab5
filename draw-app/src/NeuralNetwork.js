import axios from 'axios';

const NeuralNetwork = {
  async sendImageToBackend(imageData) {
    try {
      const response = await axios.post('http://localhost:8000/inbetweener/api/analyze/', { image: imageData });
      console.log('Backend response:', response.data);
      return response.data;
    } catch (error) {
      console.error('Ошибка при отправке изображения на бэкенд', error);
    }
  },
};

export default NeuralNetwork;
