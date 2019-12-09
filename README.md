[![Build Status](https://travis-ci.com/RENCI/tx-logging.svg?token=hSyYs1SXtzNJJDmjUzHi&branch=master)](https://travis-ci.com/RENCI/tx-logging)

# tx-logging

### run

```
docker-compose -f docker-compose.yml -f volume/docker-compose.yml up --build
```

### test
```
docker-compose -f docker-compose.yml -f volume/docker-compose.yml -f test/docker-compose.yml up --build -V --exit-code-from txlogging-test
```

### examples
Log a message with minimal fields (e.g., no 'level', 'source', or 'message' fields) and add a custom field, "foo"
```
 curl --header "Content-Type: application/json" -d "{\"_id\": \"testid7\",  \"timestamp\": \"2019-09-20\", \"event\": \"this is a test event\",   \"foo\": \"bar\" }" http://localhost:8080/lo
 ```
 
 List all messages in the log (take care if the log is large)
 ```
 curl "http://localhost:8080/log"|sed -s 's/}}/}}\n/g'
 ```
 
 List all messages with 'timestamp' between 2019-09-21 (notice 'end' is exclusive)
 ```
  curl "http://localhost:8080/log?start=2019-09-21&end=2019-09-22"|sed -s 's/}}/}}\n/g'
  ```
  
 List all messages with 'timestamp' after 2019-09-20
 ```
  curl "http://localhost:8080/log?start=2019-09-20|sed -s 's/}}/}}\n/g'
  ```
