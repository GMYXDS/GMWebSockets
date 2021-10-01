from GMWebSockets.Api import *

# route
sec_route = [
    (r"/status", StatusHandler)
]
# ip
address='127.0.0.1'
# port
port = 8080
# 超时信息
time_out_message = '{"type":"ping"}'
# 心跳间隔
time_out_interval = 15
# 超时次数
time_out_times = 3
# 验证超时时间
auth_timeout= 15

# redis
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_PASSWORD = ""

# mysql
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"