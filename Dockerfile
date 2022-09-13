FROM python:3.8.13-buster

WORKDIR /app

COPY ./ ./

ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get -y install ffmpeg libsm6 libxext6 \
  && pip install --upgrade pip \
  && pip install -e . \
  && pip install -r requirements.txt

CMD streamlit run Home.py
