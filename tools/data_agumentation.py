#!/usr/bin/env python3

#  This is to augment the data
from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from keras.preprocessing.image import ImageDataGenerator
from skimage import io

datagen = ImageDataGenerator(
    rotation_range=45,        # Random rotation between 0 and 45
    width_shift_range=0.2,    # % shift
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='reflect'   # options can be: nearest, constant, reflect, wrap
)

i = 0
for batch in datagen.flow_from_directory(
        directory='media/3d_printer/',
        classes=['bad'],
        batch_size=32,
        target_size=(448, 360),
        color_mode="rgb",
        save_to_dir='media/3d_printer/bad_aug/',
        save_prefix='aug',
        save_format='png'):
    i += 1
    if i > 32:
        break
