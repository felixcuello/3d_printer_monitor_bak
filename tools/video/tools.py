import cv2
from utils.logger import *

def get_frames(output_directory, filename, frame_name, sample_rate_ms):
    log_info("Getting frames")
    log_info("Sample rate {}".format(sample_rate_ms))
    log_info("Using CV2 {}".format(cv2.__version__))

    count = 0
    vidcap = cv2.VideoCapture(filename)
    success,image = vidcap.read()
    success = True
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*int(sample_rate_ms)))    # added this line
        success,image = vidcap.read()
        if not success:
            break

        image = crop_image(image, 15, 0)
        image = convert_to_bw(image)

        cv2.imwrite( output_directory + "{}_{}.jpg".format(frame_name, count), image)     # save frame as JPEG file
        count = count + 1

    log_info("{} images read".format(count))

# This function crops symmetrically left/right and top/bottom given a percentage
def crop_image(image, x_percent, y_percent):
    height, width, channels = image.shape

    down = int(height * y_percent / 100)
    up = height - down
    left = int(width * x_percent / 100)
    right = width - left

    return image[down:up, left:right]

# Just convert to black and white
def convert_to_bw(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
