FROM python:3.10-slim

RUN apt-get update && apt-get upgrade -y && apt-get install curl -y

WORKDIR /backend

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]