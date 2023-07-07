FROM python:3.11

ARG TESTHOMEDIR=/opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH $TESTHOMEDIR

WORKDIR $TESTHOMEDIR

COPY requirements.txt .

RUN  pip install --no-cache-dir --upgrade pip \
     && pip install --no-cache-dir --requirement requirements.txt

COPY . .
