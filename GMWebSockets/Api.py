import tornado.ioloop
import tornado.web
from tornado.escape import json_encode

from GMWebSockets.Utils import *


class StatusHandler(tornado.web.RequestHandler):
    def get(self):
        global allsockets
        online_num = len(allsockets.keys())

        # 返回文字
        # self.write("Hello, world")
        # self.write("现在的在线人数为：")
        # self.write(str(len(allsockets.keys())))

        # 返回json
        self.finish({'online_num': online_num})