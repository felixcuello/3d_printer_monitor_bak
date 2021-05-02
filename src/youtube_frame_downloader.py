from youtube.downloader import yt_download
from video.tools import get_frames
from utils.logger import *
import sys

if len(sys.argv) != 3:
    print()
    print("Usage: ")
    print("     {} <youtube_url> <frame_names>".format(sys.argv[0]))
    print()
    exit(1)

# desired_video = "https://www.youtube.com/watch?v=OaSwzjjVid4" # 3d printer video
# desired_video = "https://www.youtube.com/watch?v=bH6OGXNUCC0" # sample SHORT video
desired_video = sys.argv[1]

video_output_directory = "/app/media/youtube/"
images_output_directory = "/app/media/images/"

filename = yt_download(desired_video, video_output_directory)
log_info("File was saved in {}".format(filename))

get_frames(images_output_directory, filename, sys.argv[2])
