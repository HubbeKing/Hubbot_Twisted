FROM python:3.6-slim

RUN apt update && apt install -y \
    build-essential \
    libmariadb-dev  \
    curl \
    git

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN git remote set-url origin https://github.com/HubbeKing/Hubbot_Twisted.git

HEALTHCHECK CMD curl --max-time 5 -ILs --fail http://localhost:9999 || exit 1

ENTRYPOINT ["python", "-u", "app.py"]
