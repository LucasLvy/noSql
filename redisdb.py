from mySQL_data_collector import collect_data
import redis
from datetime import datetime
def main():
    data = collect_data()
    r = redis.Redis()
    time = datetime.now().strftime("%Y-%m-%dT%H")
    for [id, event_type, occurredOn, version, graph_id, nature, object_name, paths] in data:
        values=dict({})
        for path in paths:
            r.incr(path)
            values[path]=1
            r.incr(path+":"+time)
        r.hmset(object_name+":states",values)

main()