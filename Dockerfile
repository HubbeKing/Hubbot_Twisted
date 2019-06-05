FROM python:3.6-alpine

RUN apk --update add \
    build-base \
    git \
    libffi-dev \
    openssl-dev \
    re2-dev

ADD . /app

WORKDIR /app

RUN pip install Cython

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]
