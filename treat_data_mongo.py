from pymongo import MongoClient
from datetime import datetime, timedelta

client = MongoClient('localhost', 27017)
db = client.files
collection = db.file


def find_path(filename):
    res = collection.find({"object_name": filename}, {"path": 1})
    result = []
    for x in res:
        result.extend(x["path"])
    return result


def last_hour():
    states = collection.distinct('path')
    result = dict({})
    for state in states:
        result[state] = collection.find({"occurredOn":
                                             {"$gte": datetime.now() - timedelta(hours=1)},
                                         "path": state},
                                        {"path": 1, "inserted": 1}).count()
    return result


def count_status():
    states = collection.distinct('path')
    result = dict({})
    for state in states:
        result[state] = collection.find({
            "path": state},
            {"path": 1, "occurredOn": 1}).count()
    return result


def is_verified(res, i):
    if res[i] == 'VERIFIED':
        return next(res, i)
    return False


def is_received(res, i):
    if res[i] == 'RECEIVED':
        return next(res, i)
    return False


def is_processed(res, i):
    if res[i] == 'PROCESSED':
        return next(res, i)
    return False


def is_consumed(res, i):
    if res[i] == 'CONSUMED':
        return next(res, i)
    return False


def is_rejected(res, i):
    if res[i] == 'REJECTED':
        return next(res, i)
    return False


def is_remedied(res, i):
    if res[i] == 'REMEDIED':
        return next(res, i)
    return False


def is_to_be_purged(res, i):
    if res[i] == 'TO_BE_PURGED':
        return next(res, i)
    return False


def is_purged(res, i):
    if res[i] == 'PURGED':
        return next(res, i)
    return False


def next(res, i):
    if i == len(res) - 1:
        return True
    if res[i] == 'RECEIVED':
        return is_verified(res, i + 1)
    if res[i] == 'VERIFIED':
        return is_processed(res, i + 1) or is_received(res, i + 1)
    if res[i] == 'PROCESSED':
        return is_consumed(res, i + 1) or is_rejected(res, i + 1) or is_received(res, i + 1)
    if res[i] == 'REJECTED':
        return is_to_be_purged(res, i + 1) or is_remedied(res, i + 1) or is_received(res, i + 1)
    if res[i] == 'TO_BE_PURGED':
        return is_purged(res, i + 1) or is_received(res, i + 1)
    if res[i] == 'CONSUMED':
        return is_to_be_purged(res, i + 1) or is_received(res, i + 1)
    if res[i] == 'REMEDIED':
        return is_processed(res, i + 1) or is_received(res, i + 1)
    if res[i] == 'PURGED':
        return is_received(res, i + 1)


def is_integre():
    filenames = sorted(collection.distinct('object_name'))
    count = 0
    for filename in filenames:
        res = find_path(filename)
        if next(res, 0):
            count += 1
        if not next(res, 0):
            next(['RECEIVED', 'VERIFIED', 'PROCESSED', 'CONSUMED', 'REJECTED', 'REMEDIED'], 0)
    return count
