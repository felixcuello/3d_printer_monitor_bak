import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

batch_size = 32
data_dir = "../media/images/"

img_width = 448
img_height = 360

print("[ii] Reading Training Images...")
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.3,
  class_names=['bad','good'],
  subset="training",
  seed=44,
  image_size=(img_height, img_width),
  batch_size=batch_size)

print("[ii] Reading Validation Images...")
val_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.3,
  class_names=['bad','good'],
  subset="validation",
  seed=44,
  image_size=(img_height, img_width),
  batch_size=batch_size)


AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

normalization_layer = layers.experimental.preprocessing.Rescaling(1./255)

normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
first_image = image_batch[0]

num_classes = 2

model = Sequential([
  layers.experimental.preprocessing.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
  layers.Conv2D(16, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(num_classes)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# epochs=10
# history = model.fit(
#   train_ds,
#   validation_data=val_ds,
#   epochs=epochs
# )

# =========================================================================
#  avoid overfitting
# =========================================================================

from tensorflow import keras

data_augmentation = keras.Sequential(
  [
    layers.experimental.preprocessing.RandomFlip("horizontal",
                                                 input_shape=(img_height,
                                                              img_width,
                                                              3)),
    layers.experimental.preprocessing.RandomRotation(0.1),
    layers.experimental.preprocessing.RandomZoom(0.1),
  ]
)

model = Sequential([
  data_augmentation,
  layers.experimental.preprocessing.Rescaling(1./255),
  layers.Conv2D(16, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Dropout(0.2),
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(num_classes)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])


epochs = 15
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

# external_image = 'https://i.pinimg.com/originals/02/86/d2/0286d29ba74a22133dc2ea638d7893d4.jpg' # BAD
# external_image = 'https://3dprintingindustry.com/wp-content/uploads/2020/04/Screenshot-25.jpg'  # BAD pikachu
# external_image = 'https://i.pinimg.com/474x/7f/8c/d9/7f8cd9c5c260893ba5730d7dfdb5d263.jpg' # BAD hexagon
# external_image = 'https://i.pinimg.com/474x/2d/5e/90/2d5e90e8dd27cf71c31912fdbb1cf93c.jpg' # GOOD alan turing
# external_image = 'https://images.theconversation.com/files/285678/original/file-20190725-136781-153x4jj.jpg' # GOOD
# external_image = 'https://cdn.britannica.com/22/206222-131-E921E1FB/Domestic-feline-tabby-cat.jpg' # GOOD - CAT
# external_image = 'https://cdn.britannica.com/w:400,h:300,c:crop/07/5207-050-5BC9F251/Gray-wolf.jpg' # BAD - DOG [ WRONG ]
external_image = 'http://cdn.akc.org/content/article-body-image/golden_puppy_dog_pictures.jpg' # BAD - DOG
external_path = tf.keras.utils.get_file('3d_test2.jpg', origin=external_image)

img = keras.preprocessing.image.load_img(
    external_path,
    target_size=(img_height, img_width)
)
img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) # Create a batch

predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

class_names=['bad','good']

import numpy as np

print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
)
