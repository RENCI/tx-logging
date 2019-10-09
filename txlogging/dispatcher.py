from fluent import sender
import os
import copy
from pymongo import MongoClient
from flask import Response
from bson.json_util import dumps
import logging

fluentd_host = os.environ["FLUENTD_HOST"]
fluentd_port = int(os.environ["FLUENTD_PORT"])
fluentd_app = os.environ["FLUENTD_APP"]
mongodb_host = os.environ["MONGO_HOST"]
mongodb_port = int(os.environ["MONGO_PORT"])
mongo_database = os.environ["MONGO_DATABASE"]
mongo_collection = os.environ["MONGO_COLLECTION"]
mongo_username = os.environ["MONGO_NON_ROOT_USERNAME"]
mongo_password = os.environ["MONGO_NON_ROOT_PASSWORD"]


logger = sender.FluentSender(fluentd_app, host=fluentd_host, port=fluentd_port, nanosecond_precision=True)
mongo_client = MongoClient(mongodb_host, mongodb_port, username=mongo_username, password=mongo_password, authSource=mongo_database)

def getLog(start=None, end=None):
    coll = mongo_client[mongo_database][mongo_collection]
    if start is not None or end is not None:
        q = {
            "timestamp": {
                k:v for k,v in [("$gte", start), ("$lt", end)] if v is not None
            }
        }
        res = coll.find(q)
    else:
        res = coll.find()

    def generate():
        for i in res:
            item = dumps(i)
            yield(item + "\n")
    return Response(generate(), mimetype="application/x-ndjson")

def postLog(body):
    log = copy.deepcopy(body)
    event = body["event"]
    timestamp = body["timestamp"]
    if not logger.emit(event, log):
        err = logger.last_error
        print(err)
        logger.clear_last_error()
        return str(err), 500
    return "log posted", 200

def deleteLog():
    coll = mongo_client[mongo_database][mongo_collection]
    coll.remove()
    return "log deleted", 200
