FROM python:3.10-slim

ENV HOME /backend
ENV PYTHONPATH ${HOME}

RUN apt-get update && apt-get upgrade -y && apt-get install curl python3-pip libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libffi-dev libjpeg-dev libopenjp2-7-dev nano -y

WORKDIR ${HOME}/

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]
