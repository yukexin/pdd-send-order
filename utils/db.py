from pymongo import MongoClient
import time
import datetime

host = 'localhost'
mongo_client = MongoClient(host, 27017)
db = mongo_client.mydb
myset = db.testset
print(mongo_client.server_info())  # 判断是否连接成功


# myset.insert_one(
#     {
#         "access_token": 'token2'
#     }
# )


def find():
    for i in myset.find():
        print(i)
        if i['timestamp']:
            now = int(time.time())
            timestamp = int(i['timestamp'])
            get_delta_hours()
        return i['access_token']


def get_delta_hours(self, t1, t2):
    dt2 = datetime.datetime.fromtimestamp(t2)
    dt2 = dt2.replace(hour=0, minute=0, second=0, microsecond=0)
    dt1 = datetime.datetime.fromtimestamp(t1)
    dt1 = dt1.replace(hour=0, minute=0, second=0, microsecond=0)
    return (dt2 - dt1).days * 24


def insert_one(obj):
    myset.insert_one(obj)

if __name__ == '__main__':
