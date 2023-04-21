FROM docker.io/library/python:3.6-slim

RUN apt update && apt install --no-install-recommends -y \
    build-essential \
    curl \
    git \
    libffi-dev \
    libmariadb-dev \
    libssl-dev \
    libre2-dev \
    pkg-config \
    sqlite3

# Cython needs to be installed/compiled manually, otherwise the re2 library fails to install
RUN pip install Cython

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

# set the remote url for the repo so the update module can work
RUN git remote set-url origin https://github.com/HubbeKing/Hubbot_Twisted.git

ENTRYPOINT ["python", "-u", "app.py"]
