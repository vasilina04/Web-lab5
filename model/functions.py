from tensorflow.keras.metrics import categorical_accuracy, top_k_categorical_accuracy, categorical_crossentropy
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import MobileNet
import pandas as pd
from PIL import Image, ImageOps
import numpy as np

from config import *


# Функция инициализации модели
def init_model():
    def top_3_accuracy(y_true, y_pred):
        return top_k_categorical_accuracy(y_true, y_pred, k=3)

    model = MobileNet(input_shape=(size, size, 1), alpha=1., weights=None, classes=NCATS)
    model.compile(optimizer=Adam(lr=0.002), loss='categorical_crossentropy',
                  metrics=[categorical_crossentropy, categorical_accuracy, top_3_accuracy])
    # загрузка весов в модель
    model.load_weights('model.h5')
    return model


def preds2catids(predictions):
    return pd.DataFrame(np.argsort(-predictions, axis=1)[:, :3], columns=['a', 'b', 'c'])


# предсказывание результата
# Первый параметр это модель, второй - это путь до изображения которое надо предсказать
def predict_image(model, file_path):
    img = Image.open(file_path)
    img = img.resize((64, 64))
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
