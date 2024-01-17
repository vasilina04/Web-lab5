from tensorflow.keras.metrics import categorical_accuracy, top_k_categorical_accuracy, categorical_crossentropy
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import MobileNet
import pandas as pd
from PIL import Image, ImageOps
import numpy as np
import base64
from io import BytesIO
import os

from .config import *


# Функция инициализации модели
def init_model():
    def top_3_accuracy(y_true, y_pred):
        return top_k_categorical_accuracy(y_true, y_pred, k=3)

    model = MobileNet(input_shape=(size, size, 1), alpha=1., weights=None, classes=NCATS)
    model.compile(optimizer=Adam(lr=0.002), loss='categorical_crossentropy',
                  metrics=[categorical_crossentropy, categorical_accuracy, top_3_accuracy])
    # загрузка весов в модель
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model.h5')
    model.load_weights(model_path)
    return model


def preds2catids(predictions):
    return pd.DataFrame(np.argsort(-predictions, axis=1)[:, :3], columns=['a', 'b', 'c'])


# предсказывание результата
# Первый параметр это модель, второй - это путь до изображения которое надо предсказать
def predict_image(file_path):
    model = init_model()

    img = Image.open(file_path)
    img = img.resize((64, 64))
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    img = ImageOps.invert(img)
    img = ImageOps.grayscale(img)

    img_arr = np.asarray(img)

    img_data = []
    for i in range(len(img_arr)):
        arr_to_append = [[x / 127.5 - 1] for x in img_arr[i]]
        img_data.append(arr_to_append)

    img_data = np.array([img_data])

    test_predictions = model.predict(img_data, verbose=0)

    top3 = preds2catids(test_predictions)

    cats = all_cats
    id2cat = {k: cat.replace(' ', '_') for k, cat in enumerate(cats)}
    top3cats = top3.replace(id2cat)

    return top3cats['a'][0]

def predict_image_from_base64(base64_string):
    base64_string = base64_string.split(',')[1]
    # Преобразование Base64 строки в изображение
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))

    # Получение пути к текущей папке скрипта
    script_directory = os.path.dirname(os.path.realpath(__file__))

    # Сохранение изображения в той же папке, где находится скрипт
    temp_image_path = os.path.join(script_directory, "temp_image.png")
    image.save(temp_image_path)

    # Предсказание результата
    result = predict_image(temp_image_path)

    # Удаление временного файла (если нужно)
    os.remove(temp_image_path)

    print(result)

    return result