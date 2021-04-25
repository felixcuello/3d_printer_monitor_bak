FROM python:3.6.13-buster

#  Install useful packages
# -------------------------------------------------------------------------
RUN apt -y update
RUN apt -y install cmake # requirements
RUN apt -y install vim # I want this


# -------------------------------------------------------------------------
COPY . /app
WORKDIR /app


#  Install libraries related to the YouTube Downloader
# -------------------------------------------------------------------------
RUN pip install --upgrade pip
RUN pip3 install -r ./src/requirements.txt

CMD /bin/bash
