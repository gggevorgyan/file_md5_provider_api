# pull official base image
FROM python:3.11.2-slim-buster

# set work directory
WORKDIR /usr/src/project

# copy project
COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /usr/src/project/web

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

