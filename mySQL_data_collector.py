import mysql.connector
import datetime


def collect_data():
    cnx = mysql.connector.connect(user='root', password='<MDP MYSQL>', database='application_pedagogique',
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()

    query = ("SELECT * from element")

    cursor.execute(query)
    data = []
    for (id, event_type, occurredOn, version, graph_id, nature, object_name, path) in cursor:
        data.append([id,
                     event_type,
                     datetime.datetime.strptime(occurredOn, "%Y-%m-%dT%H:%M:%S.%f"),
                     version,
                     graph_id,
                     nature,
                     object_name,
                     path.split()])
    cursor.close()
    cnx.close()
    return data
