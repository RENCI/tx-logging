from fluent import sender
import os
import copy
from pymongo import MongoClient
from flask import Response
from flask.json import dumps

fluentd_host = os.environ["FLUENTD_HOST"]
fluentd_port = int(os.environ["FLUENTD_PORT"])
fluentd_app = os.environ["FLUENTD_APP"]
mongodb_host = os.environ["MONGODB_HOST"]
mongodb_port = int(os.environ["MONGODB_PORT"])
mongodb_database = int(os.environ["MONGODB_DATABASE"])
mongodb_collection = int(os.environ["MONGODB_COLLECTION"])
mongodb_username = int(os.environ["MONGODB_USERNAME"])
mongodb_password = int(os.environ["MONGODB_PASSWORD"])


logger = sender.FluentSender(fluentd_app, host=fluentd_host, port=fluentd_port, nanosecond_precision=True)
mongo_client = MongoClient(mongodb_host, mongodb_port, username=mongodb_username, password=mongodb_password)

def getLog(start=None, end=None):
    coll = mongo_client[mongodb_database][mongodb_collection]
    coll.find({
        "timestamp": {
            "$ge": start,
            "$lt": end
        }
    })
    def generate():
        for i in coll:
            item = dumps(i)
            yield(item)
    return Response(generate(), mimetype="application/x-ndjson")

def postLog(body):
    log = copy.deepcopy(body)
    event = body["event"]
    timestamp = body["timestamp"]
    if not logger.emit(event, timestamp, log):
        err = logger.last_error
        print(err)
        logger.clear_last_error()
        return str(err), 500
    return "log posted", 200
