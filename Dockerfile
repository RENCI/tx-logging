FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip3 install --no-cache-dir flask pymongo fluent-logger gunicorn connexion python-dateutil jsonschema

COPY api/openAPI3 /usr/src/app/api
COPY txlogging /usr/src/app/txlogging
COPY tx-utils/src /usr/src/app

EXPOSE 8080

ENTRYPOINT ["gunicorn"]

CMD ["-w", "4", "-b", "0.0.0.0:8080", "api.server:create_app()"]
