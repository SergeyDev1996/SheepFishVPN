# pull official base image
FROM python:3.8.2-alpine

# set work directory
WORKDIR /usr/src/app

RUN echo "start docker prod"

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && pip install -U pip setuptools wheel ruamel.yaml.clib==0.2.6 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps

RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev \
                        libffi-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt

RUN ls /usr/src/app/

# copy entrypoint.sh

RUN ls /usr/src/app/

# copy project
COPY . /usr/src/app/
