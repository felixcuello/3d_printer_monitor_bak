import os
import sys
import uuid
import pytube

def yt_download(video, output_dir):
    # Prepare YouTube library
    youtube = pytube.YouTube(video)
    video = youtube.streams.first()
    out_file = video.download(output_dir)

    # Remove file
    target_file = "{}/{}.mp4".format(output_dir, uuid.uuid4())
    if os.path.exists(target_file):
        os.unlink(target_file)

    # Rename file
    os.rename(out_file, target_file)

    return target_file
