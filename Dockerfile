FROM python:3.6-slim

RUN apt update && apt install -y \
    build-essential \
    curl \
    git

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN git remote set-url origin https://github.com/HubbeKing/Hubbot_Twisted.git

ENTRYPOINT ["python", "-u", "app.py"]
