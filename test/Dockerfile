FROM python:3-alpine

RUN pip install requests pytest ndjson
RUN mkdir test

COPY test/test_logging.py /test/test_logging.py

WORKDIR test

ENTRYPOINT ["pytest"]

CMD ["-s"]

