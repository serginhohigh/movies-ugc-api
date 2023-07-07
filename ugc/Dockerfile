FROM python:3.11

ARG APPHOMEDIR
ARG USERNAME
ARG USER_UID
ARG USER_GID

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR $APPHOMEDIR

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -d $APPHOMEDIR

COPY requirements.txt .

RUN  pip install --no-cache-dir --upgrade pip \
     && pip install --no-cache-dir --requirement requirements.txt

COPY ./src .

EXPOSE 8000

USER $USERNAME

ENTRYPOINT ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]

