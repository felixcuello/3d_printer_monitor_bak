#!/usr/bin/env python3

import os
import sys
from matplotlib import pyplot
from tensorflow.keras.utils import to_categorical
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Conv2D
from tensorflow.python.keras.layers import MaxPooling2D
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.layers import Flatten
from tensorflow.keras.optimizers import SGD
from tensorflow import keras

import cv2
import tensorflow as tf

def load_image(filename):
    # load the image
    img = tf.keras.utils.load_img(filename, target_size=(200, 200))
    # convert to array
    img = tf.keras.utils.img_to_array(img)
    # reshape into a single sample with 3 channels
    img = img.reshape(1, 200, 200, 3)
    # center pixel data
    img = img.astype('float32')
    img = img - [123.68, 116.779, 103.939]
    return img

model = keras.models.load_model('3d_printer_model_working')

good = load_image('./good_test.jpg')
bad = load_image('./bad_test.jpg')

result_good = model.predict(good)
result_bad = model.predict(bad)

print(result_good)
print(result_bad)
