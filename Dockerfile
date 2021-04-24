FROM python:3.9.4-alpine

RUN apk update

RUN apk add vim

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD /bin/sh
