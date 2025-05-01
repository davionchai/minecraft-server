FROM python:3.12.10-slim-bookworm

WORKDIR /app

RUN apt-get update \ 
    && apt-get install -y cron \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /app

ENTRYPOINT ["python", "./main.py"]
