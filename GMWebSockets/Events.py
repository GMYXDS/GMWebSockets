
from GMWebSockets.Utils import *
from GMWebSockets.m_singledb import SingleDB


class Events():
    @staticmethod
    def onConnet(socket):
        print("event connect")

    @staticmethod
    def onMessage(socket,json_data):
        global allclients,allsockets
        print("event message")

        type = json_data['type']
        data = json_data['data']

        if type == "send_to_client":
            # user = allsockets[allclients[data['client_id']]]
            # message = data['message']
            # return user.write_message(message)
            return send_to_client(data['client_id'],data['message'])
        elif type == "send_to_socket":
            # user_id = int(data['socket_id'])
            # user = allsockets[user_id]
            # message = data['message']
            # return user.write_message(message)
            return send_to_socket(int(data['socket_id']),data['message'])
        elif type == "send_to_all":
            socket_id = str(socket.socket_id)
            if not hasattr(socket,'client_id'):
                client_id = "<not bind>"
            else:
                client_id = str(socket.client_id)
            message = "socket_id:" + socket_id + "client_id:" + client_id + "send to all :" + data['message']
            return send_to_all(message)
        elif type == "test_mysql":
            conn = SingleDB().getmysql()
            conn.select_db('mysql')
            cursor = conn.cursor()
            cursor.execute("select * from user")
            res = str(cursor.fetchone())
            print(res)
            socket.write_message(res)
        elif type == "test_redis":
            r = SingleDB().getredis(1)
            print(r)
            r.set('gm', '1234')
            res = str(r.get('gm'))
            socket.write_message(res)
        else:
            return socket.write_message(u'{"type":"not match"}')

    @staticmethod
    def onClose(socket):
        print("event close")
        pass