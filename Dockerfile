FROM python:3.6-slim

RUN apt update && apt install -y \
    build-essential \
    git \
    libre2-dev

WORKDIR /app

ADD . /app

RUN pip install Cython && pip install -r requirements.txt

RUN git remote set-url origin https://github.com/HubbeKing/Hubbot_Twisted.git

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "-u", "app.py"]
