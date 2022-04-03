# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV ACCESS_KEY="ADD YOUR IAM USER ACCESS_KEY HERE"
ENV SECRET_ACCESS_KEY="ADD YOUR IAM USER SECRET_ACCESS_KEY HERE"
ENV BUCKET_NAME="ADD YOUR BUCKET NAME HERE"

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]