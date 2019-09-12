FROM python:3.7-alpine

WORKDIR /app
ADD . .

ENV PIP_NO_BINARY=psycopg2

RUN apk add --no-cache --virtual build \
      build-base && \
    apk add --no-cache \
      postgresql-dev && \
    pip install gunicorn pipenv && \
    pipenv install --system --deploy --ignore-pipfile && \
    apk del --no-cache build
