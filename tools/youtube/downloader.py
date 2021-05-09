import os
import sys
import uuid
import pytube
from utils.logger import *

def yt_download(video, output_dir, video_quality):
    if video_quality == None:
        video_quality = "480p"

    log_info("Downloading youtube video {}".format(video))
    # Prepare YouTube library
    youtube = pytube.YouTube(video)
    video = youtube.streams.filter(res=video_quality).first()
    out_file = video.download(output_dir)

    # Remove file
    #target_file = "{}/{}.mp4".format(output_dir, uuid.uuid4())
    target_file = "{}/temp.mp4".format(output_dir) # remove this line and replace it with the above one
    if os.path.exists(target_file):
        os.unlink(target_file)

    # Rename file
    os.rename(out_file, target_file)

    return target_file
