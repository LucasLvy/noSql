import pandas as pd
import json
import pymysql

def main():
    path = 'jeuDeDonnees_1.log'

    log_data = open(path, 'r')
    result = {}
    i = 0
    for line in log_data:
        columns = line.split(',')  # or w/e you're delimiter/separator is
        columns[7] = ''.join(columns[7:]).rstrip()
        columns = columns[:8]
        columns[7] = columns[7][:-1]
        data = {}
        for c in columns:
            key = c.split('"')[1].rstrip()
            value = int(c.split('"')[2].strip(':"[]')) if key == 'version' else c.split('"')[3].strip('"[]')
            data[key] = value
        result[i] = data
        i += 1
    j = json.dumps(result)
    with open('data.json', 'w') as outfile:
        json.dump(j, outfile)
    df = pd.read_json(j, orient='index')

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='laviecestnul',
                                 db='application_pedagogique')
    df = df.rename(columns={'event-type': 'event_type', 'graph-id': 'graph_id', 'object-name': 'object_name'})
    cursor = connection.cursor()
    cols = "`,`".join([str(i) for i in df.columns.tolist()])
    # Insert DataFrame recrds one by one.
    for i, row in df.iterrows():
        sql = "INSERT INTO `element` (`" + cols + "`) VALUES (" + "%s," * (len(row) - 1) + "%s)"
        cursor.execute(sql, tuple(row))

        # the connection is not autocommitted by default, so we must commit to save our changes
        connection.commit()
