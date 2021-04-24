import pytube

desired_video = "https://www.youtube.com/watch?v=OaSwzjjVid4"

youtube = pytube.YouTube(desired_video)

video = youtube.streams.first()

video.download() # In Same Folder
