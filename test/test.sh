#!/bin/bash
docker-compose -f docker-compose.test.yml up --build -V --exit-code-from sut
