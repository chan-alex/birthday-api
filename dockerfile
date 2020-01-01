FROM python:3.7-alpine

RUN apk add bash

RUN adduser -D appuser

WORKDIR /home/appuser

COPY code/requirements-deploy.txt requirements-deploy.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements-deploy.txt
RUN venv/bin/pip install gunicorn

COPY code ./

RUN chown -R appuser:appuser ./
USER appuser

COPY docker/boot.sh ./

USER root
RUN chmod +x boot.sh

USER appuser
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
