[![Build Status](https://travis-ci.com/RENCI/tx-logging.svg?token=hSyYs1SXtzNJJDmjUzHi&branch=master)](https://travis-ci.com/RENCI/tx-logging)

# tx-logging

### run

The container requires certain volumes to be declared in the docker-compose and environmental variables that are custom to your project. You should specify these outside of the github repo source base, such as in a directory like `../build`.

For example:
1. You might create a docker-compose file (e.g., `../build/docker-compose.volumes.yml`), with the following content:
```
version: '3'
    
volumes:
  txlogging-mongo-data:
    driver: local
```
2. You might create a file with a set of bash commands (e.g., `../build/env.src`) that can be sourced (e.g., `. ../build/env.src`) to pull in values for all the variables in the root docker-compose.yml file:
```
export MONGO_HOST=txlogging-mongodb
export MONGO_PORT=27017
export MONGO_DATABASE=txloggingdb
export MONGO_COLLECTION=log
export MONGO_INITDB_ROOT_USERNAME=root
export MONGO_INITDB_ROOT_PASSWORD=example
export MONGO_NON_ROOT_USERNAME=txlogging
export MONGO_NON_ROOT_PASSWORD=log
export FLUENTD_CONFIG_DIR=../build/fluentd/etc
export MONGODB_DATA_VOLUME=txlogging-mongo-data
export API_PORT=8080
export FLUENTD_APP=txlogging
export FLUENTD_HOST=txlogging-fluentd
export FLUENTD_PORT=24224
```
3. It would also be a good idea to create a file to unset thoes variables (e.g., `../build/env-unset.src`):
```
unset MONGO_HOST
...

```

4. Given the above examples:

The container can be deployed, tested from the command-line, and stopped with:
```
source ../build/env.src
docker-compose -f docker-compose.yml -f ../build/docker-compose.volumes.yml up --build -V -d
curl --header "Content-Type: application/json" -d "{ \"timestamp\": \"2019-09-20T00:00:00Z\", \"level\": \"1\", \"source\": \"some source\", \"event\": \"this is a test event\",   \"foo\": \"bar\" }" localhost:8080/log
docker-compose -f docker-compose.yml -f ../build/docker-compose.volumes.yml down
```
The full test run by dockerhub during CI/CD can also be run from the comand-line as follows (assumes the existence fo ./build/env-unset.src, see examples above):
```
source ../build/env-unset.src
 docker-compose -f docker-compose.test.yml up --build -V
```
The above command will not detach and must be ended with ^C. If the test fails, see troubleshooting section below.

```
docker-compose -f docker-compose.yml -f volume/docker-compose.yml up --build -d
# bring it back down (WARNING: logs do persist, and logging messages may affect docker-compose.test.yml results if run on the same machine):
docker-compose down
```

### test
```
docker-compose -f docker-compose.test.yml up --build -V 
```

### examples
Log a message with minimal fields (e.g., no 'message' field) and add a custom field, "foo"
```
curl --header "Content-Type: application/json" -d "{ \"timestamp\": \"2019-09-20T00:00:00Z\", \"level\": \"1\", \"source\": \"some source\", \"event\": \"this is a test event\",   \"foo\": \"bar\" }" localhost:8080/log
 ```
 
 List all messages in the log (take care if the log is large)
 ```
 curl "http://localhost:8080/log"|sed -s 's/}}/}}\n/g'
 ```
 
 List all messages with 'timestamp' between 2019-09-21 (notice 'end' is exclusive)
 ```
 # includes new log entry from example above
  curl "http://localhost:8080/log?start=2019-09-20T00:00:00Z&end=2019-09-22T00:00:00Z"|sed -s 's/}}/}}\n/g'
 # no example log entry
  curl "http://localhost:8080/log?start=2019-09-21T00:00:00Z&end=2019-09-22T00:00:00Z"|sed -s 's/}}/}}\n/g'
  ```
  
 List all messages with 'timestamp' after 2019-09-20
 ```
  curl "http://localhost:8080/log?start=2019-09-20|sed -s 's/}}/}}\n/g'
  ```

## Troubleshooting

# Test fails: `requests.get` 

You may run the following:
```
sut_1                |         resp2 = requests.get("http://txlogging:8080/log", params={
...
sut_1                | E       assert 2 == 1
```
where '2' is some number bigger than 1. The full message is below. You mayget this error if you logged a message and then ran the test on the same machine.

For example, this error will result from the following sequence of commands:
```
docker-compose -f docker-compose.yml -f ../build/docker-compose.volumes.yml up --build -V -d
curl --header "Content-Type: application/json" -d "{ \"timestamp\": \"2019-09-20T00:00:00Z\", \"level\": \"1\", \"source\": \"some source\", \"event\": \"this is a test event\",   \"foo\": \"bar\" }" localhost:8080/log
docker-compose -f docker-compose.yml -f ../build/docker-compose.volumes.yml down
docker-compose -f docker-compose.test.yml up --build -V
```

__WARNING: do not do the following on a production or shared server, it will affect all users, proceed with caution__

To resolve the test error, remove the persistent log by pruning any unused images, containers and volumes:
```
docker image prune -af
docker container prune -f
docker volume prune -f
```

One way to remove persistent logs is to remove all the containers and images on your sandbox, starting clean:

__WARNING: do not do the following on a production or shared server, it will affect all users, proceed with caution__

```
docker container rm -f $(docker container list -aq)
docker rmi -f $(docker images -aq)
docker container prune -f
docker image prune -af
docker volume prune -f
docker system prune -af
```

The full error message follows
```
sut_1                | test_logging.py F
sut_1                |
sut_1                | =================================== FAILURES ===================================
sut_1                | _________________________________ test_logging _________________________________
sut_1                |
sut_1                |     def test_logging():
sut_1                |
sut_1                |         resp1 = requests.post("http://txlogging:8080/log", json=msg)
sut_1                |
sut_1                |         assert resp1.status_code == 200
sut_1                |
sut_1                |         time.sleep(10)
sut_1                |
sut_1                |         resp2 = requests.get("http://txlogging:8080/log", params={
sut_1                |         })
sut_1                |
sut_1                |         assert resp2.status_code == 200
sut_1                | >       assert len(ndjson.loads(resp2.text)) == 1
sut_1                | E       assert 2 == 1
sut_1                | E        +  where 2 = len([{'_id': {'$oid': '5dffea3db1eefc000e5c75cf'}, 'event': 'this is a test event', 'fluentd_time': {'$date': 157705273146...9486e'}, 'comments': 'this is a comments', 'event': 'this is an event', 'fluentd_time': {'$date': 1577052779642}, ...}])
sut_1                | E        +    where [{'_id': {'$oid': '5dffea3db1eefc000e5c75cf'}, 'event': 'this is a test event', 'fluentd_time': {'$date': 157705273146...9486e'}, 'comments': 'this is a comments', 'event': 'this is an event', 'fluentd_time': {'$date': 1577052779642}, ...}] = <function loads at 0x7f4e78445d30>('{"_id": {"$oid": "5dffea3db1eefc000e5c75cf"}, "timestamp": "2019-09-20T00:00:00+00:00", "level": "1", "source": "some...:00+00:00", "comments": "this is a comments", "level": "0", "source": "a", "fluentd_time": {"$date": 1577052779642}}\n')
sut_1                | E        +      where <function loads at 0x7f4e78445d30> = ndjson.loads
sut_1                | E        +      and   '{"_id": {"$oid": "5dffea3db1eefc000e5c75cf"}, "timestamp": "2019-09-20T00:00:00+00:00", "level": "1", "source": "some...:00+00:00", "comments": "this is a comments", "level": "0", "source": "a", "fluentd_time": {"$date": 1577052779642}}\n' = <Response [200]>.text
sut_1                |
sut_1                | test_logging.py:25: AssertionError
sut_1                | !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
sut_1                | ============================== 1 failed in 10.91s ==============================
tx-logging_sut_1 exited with code 1
```