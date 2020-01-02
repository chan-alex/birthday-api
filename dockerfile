FROM python:3.7-alpine

RUN apk add nginx 

RUN adduser -D appuser
USER appuser

WORKDIR /home/appuser
COPY code/requirements-deploy.txt requirements-deploy.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements-deploy.txt
RUN venv/bin/pip install gunicorn
COPY code ./
COPY docker/boot.sh ./

USER root
RUN chmod +x boot.sh
COPY docker/nginx.conf /etc/nginx/nginx.conf

RUN chown -R appuser:appuser ./

# simple method to allow appuser to start up nginx.
RUN mkdir /run/nginx && chown -R appuser.appuser /run && \
  chown -R appuser.appuser /var/lib/nginx && \
  chown -R appuser.appuser /var/log/nginx

USER appuser
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
