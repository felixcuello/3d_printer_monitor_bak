# 3d Printer Monitor

# Introduction

The goal of this project is to create a monitoring software that can monitor a 3d printer and detect anomalies.

The monitoring software must use computer vision to detect these anomalies and produce a programmed response given the anomaly detected.

This response can be configurable like stopping the machine or sending a message to alert the problem.

We will define an "anomaly" when the 3d printer goes off course of the model that has to be printed.

Below you'll find a few examples of anomalies. Probably further in this investigation we will find more:

- Excess of filament producing problems
- Model flipped
- Problems in the model printed
- ...



# Libraries

## Keras

The first quick research on the topic of "image recognition" and "image classification" led me to Keras.

From the [keras.io webpage](https://keras.io/about/) we can quote:

_"Keras is a deep learning API written in Python, running on top of the machine learning platform TensorFlow."_

_"Keras is the high-level API of TensorFlow 2: an approachable, highly-productive interface for solving machine learning problems, with a focus on modern deep learning. It provides essential abstractions and building blocks for developing and shipping machine learning solutions with high iteration velocity."_



## Tensorflow

Tensorflow, in the other hand, is an open source machine learning library that can be used from many languages.


# Docker Containers

To avoid polluting the host computer with unnecessary software we will work inside a docker container as much as possible.

## Building the container

Building the container is quite easy, thanks to the `docker-compose` tool.

The following command will  build the `3d_printer_monitor` container with all the tools and apps required to run it.

``` sh
docker-compose build
```



# Tools in the container
tools/youtube_video_sampler
Once the container is built. There are some tools already coded in the container.

## YouTube Video Downloader

The YouTube Video Downloader (`tools/youtube_video_downloader`) is a tool that permits you to download youtube videos.

The parameters are positional and are self explanatory:

``` sh

Usage:
     tools/youtube_video_downloader <youtube_url> [YouTube video quality]

     YouTube Video Quality: 144p, 240p, (360p) default, 480p, 720p, 1080p
     
```

## Video Splitter

The Video Splitter (`tools/video_splitter`) is a tool that permits you to split videos into frames.

The parameters are also self explanatory:

``` sh

Usage:
     tools/video_splitter <video_path> <frame_names> [sample_rate_ms]

     sample_rate_ms default is 250ms

```


## Split Cateogries in Training / Test sets

The Split Categories script split training/test set into directories to feed the convolutional neural network:

``` sh

Usage:
     ./tools/split_training_set <media_directory> <csv_categories> [test_percentage]
     (default training: 20%)

```

An example of usage can be like this: `./tools/split_training_set media/images "bad,good"`


# Machine Learning

In any maachine learning project, the process of carefully selecting the learning data is one of the most tedious processes.

For this phase of the process we want to identify only TWO things:

- **Printing is going GOOD**: This means the printer shouldn't be stopped, and the printer is working as expected.

- **Printing is having a PROBLEM**: A problem has been detected and the printer must be stopped and the user should be notified.



# Step 1: Simple image classification

Here we need to describe how to build a simple image classification (i.e. something good / something bad)

## Getting the images

Like any other ML project focused on image recognition we need to get a large amount of images of 3d printers doing both a good and a bad job. After looking online for some resources like Google Images, I couldn't find easily a set of images with good / bad printing exmaples.

I've been doing that for a while, until I realized that perhaps a good source of images aren't IMAGES itself, but videos. Since videos are a sequence of images, perhaps I can do this:

1. Get videos from youtube
2. Split videos into images
3. Crop the images
4. Classify them as Good or Bad images


## Step 2: Find a simple way to get images

For this purpose we realized that a good source and diverse images are YouTube videos, since there are plenty of people showing their printings in timelapses.

The steps for this are:

1. **SELECT VIDEOS**: Select several videos where we can capture videos about 3d printing with good and bad results:
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

The very first step on this project is to get as many images as possible tagged as **GOOD** printings and **BAD** printings.

These images are going to be catalogued here:

- `/media/images/good`: Are the images representing **GOOD** printings

- `/media/images/bad`: Are the images representing **BAD** printings

## Downloading and tagging the sources

By using the [YouTube Video Sampler tool](tools/youtube_video_sampler) explained in the previous section, we will download several Youtube videos tagging the images as either **GOOD** or **BAD**.

Following sections are listing videos used for getting Good and Bad Images

### Good

- (GEA001) https://www.youtube.com/watch?v=aubLuCFIejc
- (G-0002) https://www.youtube.com/watch?v=54ZKeYPmoVs
- (G-0003) https://www.youtube.com/watch?v=bgHoQ_5dT2M
- (G-0004) https://www.youtube.com/watch?v=zBuFs-Hupto
- (G-0005) https://www.youtube.com/watch?v=VFQeV8m9HQo
- (G-0006) https://www.youtube.com/watch?v=Dss1yUHH-QY
- (G-0007) https://www.youtube.com/watch?v=dlt8ObxzoHQ
- (G-0008) https://www.youtube.com/watch?v=Jizyu0nGH18
- (G-0009) https://www.youtube.com/watch?v=uBeVbDJKHw0
- (G-0010) https://www.youtube.com/watch?v=qpv4-tfkipw

### Bad

- (B-0001) https://www.youtube.com/watch?v=JGpCGOMgk5g
- (B-0002) https://www.youtube.com/watch?v=ZmS-3Kcti10
- (B-0003) https://www.youtube.com/watch?v=uzKMV_O42SY
- (B-0004) https://www.youtube.com/watch?v=4Y8bPODaEk4
- (B-0005) https://www.youtube.com/watch?v=305lLo2FcfQ
- (B-0006) https://www.youtube.com/watch?v=ZBWBVMABR0w
- (B-0007) https://www.youtube.com/watch?v=WZugigyVyrA
- (B-0008) https://www.youtube.com/watch?v=i583-DYivpA
- (B-0009) https://www.youtube.com/watch?v=8zB2mlJXeHU
- (B-0010) https://www.youtube.com/watch?v=hCxdupxs1Ng

## Step 3: Create Standar Representation of Images

According to Keras documentation:

_Neural networks don't process raw data, like text files, encoded JPEG image files, or CSV files. They process vectorized & standardized representations_

Therefore we need to normalize the images before using them.

## Step 4: Data Agumentation


# Reading Material

- [Basic Image Classification](https://www.tensorflow.org/tutorials/keras/classification)
- [Keras - deep learning library for Python](https://keras.io/)
- [Introduction to Keras for Engineers](https://keras.io/getting_started/intro_to_keras_for_engineers/)
- [Image Classification From Scratch](https://keras.io/examples/vision/image_classification_from_scratch/)
- [Building a powerful image classification](https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html)
- [Transfer learning and fine tunning](https://keras.io/guides/transfer_learning/)


# --------------------------------------------------------------------------------------
## ALL STEPS BELOW THIS POINT ARE PENDING
# --------------------------------------------------------------------------------------


## Step 4: Train + Test the model

Train and test the model, and see if the model gets a higher (>75% of accuracy).

## Step 5: Build a simple application that can take snapshots at a 3d printer

We need to build a software that can take snapshots of a 3d printing machine and determine the machine status (i.e. GOOD vs. BAD state of the machine at a given moment).

## Step 6: Build a simple notification system

This could be a something like an e-mail or just send a signal somewhere to alert.

