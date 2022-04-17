FROM python:3.6.13-buster

#  Install useful packages
# -------------------------------------------------------------------------
RUN apt -y update
RUN apt -y install cmake                        # requirements
RUN apt -y install vim                          # I want this
RUN apt -y install ffmpeg libsm6 libxext6       # Required by CV2

# -------------------------------------------------------------------------
COPY . /app
WORKDIR /app

#  Install libraries related to the YouTube Downloader
# -------------------------------------------------------------------------
RUN pip install --upgrade pip
RUN pip3 install -r ./requirements.txt

CMD /bin/bash
