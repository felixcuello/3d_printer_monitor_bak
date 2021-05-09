import cv2
from utils.logger import *

def get_frames(output_directory, filename, frame_name, sample_rate_ms):
    log_info("Getting frames")
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
        cv2.imwrite( output_directory + "{}_{}.jpg".format(frame_name, count), image)     # save frame as JPEG file
        count = count + 1

    log_info("{} images read".format(count))
