import txlogging.dispatcher

def getLog(start=None, end=None):
    return txlogging.dispatcher.getLog(start, end)

def postLog(body):
    return txlogging.dispatcher.postLog(body)

def deleteLog():
    return txlogging.dispatcher.deleteLog()

