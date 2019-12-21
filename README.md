[![Build Status](https://travis-ci.com/RENCI/tx-logging.svg?token=hSyYs1SXtzNJJDmjUzHi&branch=master)](https://travis-ci.com/RENCI/tx-logging)

# tx-logging

### run

```
docker-compose -f docker-compose.yml -f volume/docker-compose.yml up --build -d
# bring it back down:
docker-compose down
```

### test
```
docker-compose -f docker-compose.test.yml up --build -V 
```

### examples
Log a message with minimal fields (e.g., no 'level', 'source', or 'message' fields) and add a custom field, "foo"
```
curl --header "Content-Type: application/json" -d "{ \"timestamp\": \"2019-09-20T00:00:00Z\", \"level\": \"1\", \"source\": \"some source\", \"event\": \"this is a test event\",   \"foo\": \"bar\" }" localhost:8080/log
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
