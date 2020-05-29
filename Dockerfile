FROM python:3.6-alpine

RUN apk --update add \
    build-base \
    curl \
    git \
    libffi-dev \
    mariadb-connector-c-dev \
    openssl-dev \
    re2-dev \
    sqlite

# Cython needs to be installed/compiled manually, otherwise the re2 library fails to install
RUN pip install Cython

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

RUN git remote set-url origin https://github.com/HubbeKing/Hubbot_Twisted.git

HEALTHCHECK CMD curl --max-time 5 -ILs --fail http://localhost:9999 || exit 1

ENTRYPOINT ["python", "-u", "app.py"]
