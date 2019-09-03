FROM python:3.7-alpine

WORKDIR /app
ADD . .

ENV PIP_NO_BINARY=psycopg2

RUN pip install pipenv && \
    pipenv install --system --deploy && \
    pip install gunicorn
