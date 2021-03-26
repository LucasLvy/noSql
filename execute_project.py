import injector
import mongodb
import redisdb
import treat_data_mongo as m
import treat_data_redis as r
import time
while True:
    try:
        injector.main()
    except:
        print("Couldn't add the date to the sql database probably because they are duplicates")
    try:
        mongodb.main()
    except:
        print("Couldn't add the date to the mongo database probably because they are duplicates")

    redisdb.main()

    print('File path : ' + str(m.find_path('File-79')))  # Example file
    print('Each status has : ' + str(m.count_status()) + ' files')
    print('Each status has : ' + str(m.last_hour()) + ' files that were added last hour')
    print(str(m.is_integre()) + ' files are integre')  # Example file

    print('File path : ' + str(r.find_path('File-79')))  # Example file
    print('Each status has : ' + str(r.count_status()) + ' files')
    print('Each status has : ' + str(r.last_hour()) + ' files that were added last hour')
    print(str(r.count_integre()) + ' files are integre')  # Example file
    time.sleep(300)
