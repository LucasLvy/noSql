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
    return 'CONSUMED : ' + r.get(b'CONSUMED:' + time).decode('utf-8') + ' PROCESSED : ' + r.get(
        b'PROCESSED:' + time).decode('utf-8') + \
           ' PURGED : ' + r.get(
        b'PURGED:' + time).decode('utf-8') + ' RECEIVED : ' + r.get(b'RECEIVED:' + time).decode(
        'utf-8') + ' REJECTED : ' + r.get(
        b'REJECTED:' + time).decode('utf-8') + ' REMEDIED : ' + r.get(
        b'REMEDIED:' + time).decode('utf-8') + ' TO_BE_PURGED : ' + r.get(b'TO_BE_PURGED:' + time).decode(
        'utf-8') + ' VERIFIED : ' + r.get(b'VERIFIED:' + time).decode('utf-8')


def find_path(filename):
    res = r.hgetall(filename + ":states")
    res = [k.decode('utf-8') for k, v in res.items() if v]
    return res


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


def count_integre():
    files = r.keys('File-*')
    count = 0
    res = []
    for file in files:
        res.append(file.decode('utf-8').split(sep=':')[0])
    for file in res:
        if is_integre(file):
            count += 1
        if not is_integre(file):
            is_integre(file)
    return count


def is_integre(filename):
    res = find_path(filename)
    return next(res, 0)
