# 3d Printer Monitor

## Introduction

The goal of this project is to create a monitoring software that can monitor a 3d printer and detect anomalies.

The monitoring software must use computer vision to detect these anomalies and produce a programmed response given the anomaly detected.

This response can be configurable like stopping the machine or sending a message to alert the problem.

We will define an "anomaly" when the 3d printer goes off course of the model that has to be printed.

Below you'll find a few examples of anomalies. Probably further in this investigation we will find more:

- Excess of filament producing problems
- Model flipped
- Problems in the model printed
- ...

## Keras

The first quick research on the topic of "image recognition" and "image classification" led me to Keras.

From the [keras.io webpage](https://keras.io/about/) we can quote:

_"Keras is a deep learning API written in Python, running on top of the machine learning platform TensorFlow."_

_"Keras is the high-level API of TensorFlow 2: an approachable, highly-productive interface for solving machine learning problems, with a focus on modern deep learning. It provides essential abstractions and building blocks for developing and shipping machine learning solutions with high iteration velocity."_

## Tensorflow

Tensorflow, in the other hand, is an open source machine learning library that can be used from many languages.

## Docker

To avoid polluting the host computer with unnecessary software we will work inside a docker container as much as possible.

### Building the container

To build the container you only have to:

``` sh
docker build -t 3d_printer_monitor .
```

### Running the container

``` sh
docker run -v $(pwd):/app -ti 3d_printer_monitor
```

### Accessing the container

## Step 1: Simple image classification

Here we need to describe how to build a simple image classification (i.e. something good / something bad)

### Getting the images

Perhaps one of the most tedious parts of any Machine Learning (ML) projects is to get the right set of images for training and testing.

Like any other ML project focused on image recognition we need to get a large amount of images of 3d printers doing both a good and a bad job.

For this purpose we realized that a good source and diverse images are YouTube videos, since there are plenty of people showing their printings in timelapses.

So, the steps for this are:

1. **SELECT VIDEOS**: Select several videos where we can capture good and bad videos.
   - Videos must show different 3d printers and desk configurations
   - Videos must show different models
   - Videos must show different models in different colors
   - Videos must come from different sources
   - Videos must come (ideally) from different camera resultions
   - Videos must come (ideally) from different camera models
   - All the requirements described above are to avoid overfitting
2. **TAKE IMAGE SAMPLES**: After getting the videos we should be able to take samples from them.
   - Samples must taken on regular intervals in the video (like every n seconds)
   - Samples don't have to be necessarily cropped

### Downloading and tagging the sources

We created a program based on a YouTube library to download youtube videos and also categorize them.

This software is based on `pytube` a library to interact with YouTube. The source can be found in [./src/youtube_downloader.py](./src/youtube_downloader.py)

## Step 2: Find a simple way to get images

We need to create a train / test set of images, so we can train and test our model.

## Step 3: Create Standar Representation of Images

According to Keras documentation:

_Neural networks don't process raw data, like text files, encoded JPEG image files, or CSV files. They process vectorized & standardized representations_

Therefore we need to normalize the images before using them

## Step 4: Train + Test the model

Train and test the model, and see if the model gets a higher (>75% of accuracy).

## Step 5: Build a simple application that can take snapshots at a 3d printer

We need to build a software that can take snapshots of a 3d printing machine and determine the machine status (i.e. GOOD vs. BAD state of the machine at a given moment).

## Step 6: Build a simple notification system

This could be a something like an e-mail or just send a signal somewhere to alert.

## Reading Material

- [Basic Image Classification](https://www.tensorflow.org/tutorials/keras/classification)
- [Keras - deep learning library for Python](https://keras.io/)
- [Introduction to Keras for Engineers](https://keras.io/getting_started/intro_to_keras_for_engineers/)
- [Image Classification From Scratch](https://keras.io/examples/vision/image_classification_from_scratch/)
- [Building a powerful image classification](https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html)
- [Transfer learning and fine tunning](https://keras.io/guides/transfer_learning/)
