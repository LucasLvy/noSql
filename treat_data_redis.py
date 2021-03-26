import redis
from datetime import datetime

r = redis.Redis()


def count_status():
    return 'CONSUMED : ' + r.get(b'CONSUMED').decode('utf-8') + ' PROCESSED : ' + r.get(b'PROCESSED').decode('utf-8') + \
           ' PURGED : ' + r.get(
        b'PURGED').decode('utf-8') + ' RECEIVED : ' + r.get(b'RECEIVED').decode('utf-8') + ' REJECTED : ' + r.get(
        b'REJECTED').decode('utf-8') + ' REMEDIED : ' + r.get(
        b'REMEDIED').decode('utf-8') + ' TO_BE_PURGED : ' + r.get(b'TO_BE_PURGED').decode(
        'utf-8') + ' VERIFIED : ' + r.get(b'VERIFIED').decode('utf-8')


def last_hour():
    time = datetime.now().strftime("%Y-%m-%dT%H").encode('utf-8')
    return 'CONSUMED : ' + r.get(b'CONSUMED:'+time).decode('utf-8') + ' PROCESSED : ' + r.get(b'PROCESSED:'+time).decode('utf-8') + \
           ' PURGED : ' + r.get(
        b'PURGED:'+time).decode('utf-8') + ' RECEIVED : ' + r.get(b'RECEIVED:'+time).decode('utf-8') + ' REJECTED : ' + r.get(
        b'REJECTED:'+time).decode('utf-8') + ' REMEDIED : ' + r.get(
        b'REMEDIED:'+time).decode('utf-8') + ' TO_BE_PURGED : ' + r.get(b'TO_BE_PURGED:'+time).decode(
        'utf-8') + ' VERIFIED : ' + r.get(b'VERIFIED:'+time).decode('utf-8')


def find_path(filename):
    res = r.hgetall(filename + ":states")
    return res


def is_verified(res, index, i):
    if index in res:
        if int(res[b'VERIFIED']):
            return next_value(res, index, i)
    return False


def is_processed(res, index, i):
    if index in res:
        if int(res[b'PROCESSED']):
            return next_value(res, index, i)
    return False


def is_consumed(res, index, i):
    if index in res:
        if int(res[b'CONSUMED']):
            return next_value(res, index, i)
    return False


def is_rejected(res, index, i):
    if index in res:
        if int(res[b'REJECTED']):
            return next_value(res, index, i)
    return False


def is_remedied(res, index, i):
    if index in res:
        if int(res[b'REMEDIED']):
            return next_value(res, index, i)
    return False


def is_to_be_purged(res, index, i):
    if index in res:
        if int(res[b'TO_BE_PURGED']):
            return next_value(res, index, i)
    return False


def is_purged(res, index, i):
    if index in res:
        if int(res[b'PURGED']):
            return next_value(res, index, i)
    return False


def next_value(res, index, i):
    if i == len(res) - 1:
        return True
    if int(res[index]):
        if index == b'RECEIVED':
            return is_verified(res, b'VERIFIED', i + 1)
        elif index == b'VERIFIED':
            return is_processed(res, b'PROCESSED', i + 1)
        elif index == b'PROCESSED':
            return is_consumed(res, b'CONSUMED', i + 1) or is_rejected(res, b'REJECTED', i + 1)
        elif index == b'REJECTED':
            return is_to_be_purged(res, b'TO_BE_PURGED', i + 1) or is_remedied(res, b'REMEDIED', i + 1)
        elif index == b'TO_BE_PURGED':
            return is_purged(res, b'PURGED', i + 1)
        elif index == b'CONSUMED':
            return is_to_be_purged(res, b'TO_BE_PURGED', i + 1)
        elif index == b'REMEDIED':
            return is_processed(res, b'PROCESSED', i + 1)

def count_integre():
    files = r.keys('File-*')
    count=0
    for file in files:
        if is_integre(file.decode('utf-8').split(sep=':')[0]):
            count+=1
    return count
def is_integre(filename):
    res = find_path(filename)
    return next_value(res, next(iter(res)), 0)
