FROM python:3.13-slim

WORKDIR /app
ENV PYTHONPATH=/app/src

COPY requirements.txt .

RUN apt-get update && apt-get upgrade -y && apt-get clean

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /data

COPY . .

CMD ["watchmedo", "auto-restart", "--patterns=*.py", "--recursive", "--", "python", "src/sp/main.py"]