FROM python:3.11-bullseye

WORKDIR /flask_questions/app 

COPY . /flask_questions/app

EXPOSE 5000

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1