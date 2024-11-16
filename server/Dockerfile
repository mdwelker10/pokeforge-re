FROM python:3.10-slim

RUN mdkir /app
RUN mdkir /logs

RUN apt-get update

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

# Unsure of run command at the moment
