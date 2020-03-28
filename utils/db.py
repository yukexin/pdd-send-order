from pymongo import MongoClient
import time
import datetime

host = 'localhost'
mongo_client = MongoClient(host, 27017)
db = mongo_client.mydb
myset = db.testset  # table
print(mongo_client.server_info())  # 判断是否连接成功


def find():
    access_token = 'empty'
    for i in myset.find():
        if 'timestamp' in i:
            now = int(time.time())
            timestamp = int(i['timestamp'])
            if get_delta_hours(now, timestamp) < 23:
                print(i)
                access_token = i['access_token']
                break
    return access_token


def get_delta_hours(now, timestamp):
    dt2 = datetime.datetime.fromtimestamp(timestamp)
    dt2 = dt2.replace(hour=0, minute=0, second=0, microsecond=0)
    dt1 = datetime.datetime.fromtimestamp(now)
    dt1 = dt1.replace(hour=0, minute=0, second=0, microsecond=0)
    return (dt2 - dt1).days * 24


def insert_one(obj):
    myset.insert_one(obj)


def delete_many():
    myset.delete_many({})


if __name__ == '__main__':
    delete_many()
