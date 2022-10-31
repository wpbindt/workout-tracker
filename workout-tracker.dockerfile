FROM python:3.11-slim

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN mkdir -p /srv

WORKDIR /srv
