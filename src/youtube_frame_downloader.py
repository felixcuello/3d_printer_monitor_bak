from youtube.downloader import yt_download
from video.tools import get_frames

desired_video = "https://www.youtube.com/watch?v=OaSwzjjVid4" # 3d printer video
desired_video = "https://www.youtube.com/watch?v=bH6OGXNUCC0" # sample SHORT video

output_directory = "/app/images/youtube"

# filename = yt_download(desired_video, output_directory)
filename = "/app/images/youtube/7a2d6b26-5613-4b4b-bfb1-1f7a71c5bfcf.mp4"
print("File was saved in {}".format(filename))

get_frames(output_directory, filename)
