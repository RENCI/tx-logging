import requests
import time
import ndjson

msg = {
        "event":"this is an event",
        "timestamp": "2001-01-01T00:00:00-01:00",
        "comments":"this is a comments",
        "level": "0",
        "source": "a"
    }

def test_logging():

    resp1 = requests.post("http://txlogging:8080/log", json=msg)
    
    assert resp1.status_code == 200

    time.sleep(10)

    resp2 = requests.get("http://txlogging:8080/log", params={
    })

    assert resp2.status_code == 200
    assert len(ndjson.loads(resp2.text)) == 1

    start = "2001-01-01T00:00:00-01:00"
    end = "2002-01-01T00:00:00-01:00"

    resp3 = requests.get("http://txlogging:8080/log", params={
        "start": start,
        "end": end
    })

    assert resp3.status_code == 200
    assert len(ndjson.loads(resp3.text)) == 1

    start = "2002-01-01T00:00:00-01:00"
    end = "2003-01-01T00:00:00-01:00"

    resp4 = requests.get("http://txlogging:8080/log", params={
        "start": start,
        "end": end
    })

    assert resp4.status_code == 200
    assert len(ndjson.loads(resp4.text)) == 0

    requests.delete("http://txlogging:8080/log")


def test_delete_log():
    resp1 = requests.post("http://txlogging:8080/log", json=msg)
    
    assert resp1.status_code == 200

    time.sleep(10)

    resp2 = requests.get("http://txlogging:8080/log", params={
    })

    assert resp2.status_code == 200
    assert len(ndjson.loads(resp2.text)) == 1

    resp3 = requests.delete("http://txlogging:8080/log")

    assert resp3.status_code == 200

    resp4 = requests.get("http://txlogging:8080/log", params={
    })

    assert resp4.status_code == 200
    assert len(ndjson.loads(resp4.text)) == 0

    requests.delete("http://txlogging:8080/log")


def test_add_log2():

    resp1 = requests.post("http://txlogging:8080/log", json=msg)
    
    assert resp1.status_code == 200

    resp1 = requests.post("http://txlogging:8080/log", json=msg)
    
    assert resp1.status_code == 200

    time.sleep(10)

    resp2 = requests.get("http://txlogging:8080/log", params={
    })

    assert resp2.status_code == 200
    assert len(ndjson.loads(resp2.text)) == 2

    requests.delete("http://txlogging:8080/log")


def test_add_log_id():

    resp1 = requests.post("http://txlogging:8080/log", json={
        "_id": "message id not allowed",
        **msg
    })
    
    assert resp1.status_code == 400

    requests.delete("http://txlogging:8080/log")




