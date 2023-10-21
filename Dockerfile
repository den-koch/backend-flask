FROM python:3.11.6-slim-bullseye

WORKDIR /app

ENV FLASK_APP=flask_app
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD flask run -p $PORT