import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 不限文件位置 添加环境变量
# runpath = r"F:/python_project/test/soket_test/tornado_test/"
runpath = BASE_DIR
if runpath not in sys.path:
    sys.path.insert(0, runpath)

import json
import time

import asyncio
from tornado import ioloop
from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler

# 引入配置文件
from GMWebSockets.Config import *

from GMWebSockets.Events import Events
from GMWebSockets.Utils import *

class GMWebSocket(WebSocketHandler):
    def open(self):
        print("WebSocket opened")

        global online_num
        online_num = online_num + 1
        allsockets[self.__hash__()] = self
        self.socket_id = self.__hash__()
        self.connect_time = time.time()
        # 降低延迟
        # self.set_nodelay(True)
        
        # 开启心跳检验机制
        self.write_message(time_out_message)

        # 转发请求到事件处理
        Events.onConnet(self)

    # 处理client发送的数据
    def on_message(self, message):
        self.lastMessageTime = time.time()
        # if message == '{"type":"pong"}':
        #     self.lastMessageTime = time.time()
        #     # return self.write_message(u'{"type":"pong"}')

        try:
            json_data = json.loads(message)
        except Exception as e:
            print(e)
            return
            # return self.write_message(u'{"type":"error"}')
        # 数据json
        print(json_data)

        if json_data['type'] == "ping":
            return self.write_message(u'{"type":"pong"}')
        elif json_data['type'] == "pong":
            return
        elif json_data['type'] == "bind":
            socket_id = self.socket_id
            bind_clinet_id(socket_id,json_data['data']['client_id'])
            self.write_message(u'bind ok')
            return self.write_message(u'your hash_name is:' + str(socket_id))
        else:
            # 转发到事件处理
            Events.onMessage(self,json_data)

    def on_close(self):
        print("WebSocket closed")
        # 转发请求
        Events.onClose(self)

        global online_num, allsockets
        online_num = online_num - 1
        allsockets.pop(self.socket_id)
        if  hasattr(self,'client_id'):
            allclients.pop(self.client_id)
        # 关闭连接
        self.close()


    # 允许所有跨域通讯，解决403问题
    def check_origin(self, origin):
        return True

# -----------------------------------------------------------------

def close_sockets(socket):
    global online_num,allsockets
    # allsockets.pop(socket.socket_id)
    online_num = online_num - 1
    # if  hasattr(socket,'client_id'):
    #     allclients.pop(socket.client_id)
    # 关闭连接
    socket.close()

# 心跳定时器
def pq_watcher():
    global allsockets
    # 发送心跳
    send_to_all_sockets(time_out_message)
    # 检测
    time_now = time.time()
    for user in list(allsockets.values()):
        # 有可能该connection还没收到过消息，则lastMessageTime设置为当前时间
        if not hasattr(user,'lastMessageTime'):
            user.lastMessageTime = time.time()
            continue
        # 上次通讯时间间隔大于心跳间隔，则认为客户端已经下线，关闭连接
        if (time_now - user.lastMessageTime) > time_out_interval*time_out_times:
            # 转发请求
            Events.onClose(user)
            # 为什么这里关闭socket ,列表里的自动移除了？
            close_sockets(user)

# auth定时器
def client_check():
    global allsockets,auth_timeout
    time_now = time.time()
    for user in list(allsockets.values()):
        if not hasattr(user, 'client_id') or not user.client_id:
            # 如果15s 没有认证，就关闭连接
            if (time_now - user.connect_time > auth_timeout):
                # 提示 not auths
                user.write_message("not auth")
                # 转发请求
                Events.onClose(user)
                # 为什么这里关闭socket ,列表里的自动移除了？
                close_sockets(user)

# 控制台显示人数信息
def show_status():
    global allsockets
    print("\r"+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+": 在线人数："+str(len(allsockets.keys())),flush=True,end="")
    # print(allsockets)
    # print(allclients)
    # for item_name in allsockets.keys():
    #     print(item_name,end="\n")

# 输出基本信息
def display_ui():
    global sec_route
    print("start at : " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    print("runpath: " + BASE_DIR)
    print("wss_server listen on wss://"+address+":"+str(port))
    print("http_server listen on http://"+address+":"+str(port))
    for route in sec_route:
        print("route listen on http://"+address+":"+str(port)+route[0])

if __name__ == "__main__":
    display_ui()
    main_route = [(r"/", GMWebSocket)]
    main_route.extend(sec_route)
    application = Application(main_route)
    application.listen(port,address)
    # application.start(0)
    # 心跳循环
    ioloop.PeriodicCallback(pq_watcher, time_out_interval*1000).start()  # start scheduler 每隔2s执行一次
    # client_id-auth检测
    ioloop.PeriodicCallback(client_check, 5 * 1000).start()
    # 显示信息
    ioloop.PeriodicCallback(show_status, 5 * 1000).start()
    ioloop.IOLoop.current().start()
