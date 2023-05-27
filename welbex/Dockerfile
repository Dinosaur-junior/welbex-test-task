FROM python:3.11
ENV PYTHONUNBUFFERED 1
RUN mkdir /dino
WORKDIR /dino
COPY requirements.txt /dino/
RUN pip install -r requirements.txt
COPY welbex /dino/