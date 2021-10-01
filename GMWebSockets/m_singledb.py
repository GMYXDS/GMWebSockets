import pymysql
import redis
from GMWebSockets.Config import *

class SingleDB(object):
    instance = None
    init_flag = False

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        if SingleDB.init_flag:
            return
        print("初始化数据库单例")
        SingleDB.init_flag = True

        SingleDB.msyqlconn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, port=MYSQL_PORT, charset="utf8")
        SingleDB.redisconn0 = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASSWORD,decode_responses=True)
        SingleDB.redisconn1 = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=1, password=REDIS_PASSWORD,decode_responses=True)

    def getmysql(self):
        return SingleDB.msyqlconn

    def getredis(self,number=0):
        if(number==1):
            return SingleDB.redisconn1
        return SingleDB.redisconn0


if __name__ == '__main__':

    # 创建多个对象
    mysql1conn = SingleDB()
    print(mysql1conn)
    mysql2conn = SingleDB()
    print(mysql2conn)

    conn = SingleDB().getmysql()
    conn.select_db('mysql')
    cursor = conn.cursor()
    cursor.execute("select * from user")
    print(cursor.fetchone())

    r = SingleDB().getredis(1)
    print(r)

    r.set('gm','1234')
    print(r.get('gm'))
    print(r.get('gm'))
    print(r.get('gm'))