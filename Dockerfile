FROM python:3.6-alpine

RUN apk --update add \
    build-base \
    git \
    libffi-dev \
    openssl-dev \
    re2-dev

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir Cython && \
    pip install --no-cache-dir -r requirements.txt

RUN git remote set-url origin https://github.com/HubbeKing/Hubbot_Twisted.git

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "-u", "app.py"]
