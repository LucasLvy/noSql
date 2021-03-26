from mySQL_data_collector import collect_data
from pymongo import MongoClient

import datetime
def main():
    data=collect_data()
    mongo_data=[]
    for [id, event_type, occurredOn, version, graph_id, nature, object_name, path] in data:
        mongo_data.append({"_id": id,
                     "event_type": event_type,
                     "occurredOn": occurredOn,
                     "version": version,
                     "graph_id": graph_id,
                     "nature": nature,
                     "object_name": object_name,
                     "path": path,
                    "inserted":datetime.datetime.now()})

    client = MongoClient('localhost', 27017)
    db = client.files
    collection = db.file  # selecting the coll1 in myDatabase
    insertion = collection.insert_many(mongo_data)
    client.close()
