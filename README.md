# GMWebSockets

## 背景

最近开发需要使用websocket，但是找了一圈，发现并没有合适的

大多python封装的框架都是基于event驱动，没有connect和close 时间监听，pingpong心跳机制，认证机制，auth机制都没有，都是基于socket 的send,recieve，没有socket 管理和group 功能。

但是python的socket的框架还是挺完整的，所以基于`tornado.websocket`,我完善了相关功能，并开源此个python websocket 解决方案

## 参考

本项目使用了`tornado.websocket`模块作为基础，后续可能会升级为自己实现RFC6455协议接口

本项目还参考了workman，GatewayWorker，作为部分实现

## 简介

这是一个python的websocket框架

### 特点

- 实现的ping,pong 心跳机制
- 实现了auth，bind_id 机制
- 封装了一些send，group，session的实现
- 可以直接提供webapi操作
- 可以实现定时器操作
- 其他

## 使用说明

### 环境

```
pip install tornado
```

### 运行

```
python Server.py
```

### 目录说明

```bash
GMWebSockets
│  Api.py # 定义httpserver 开发参考tornado的web开发
│  Config.py # 定义了一些配置参数，包括监听端口，心跳间隔等
│  Events.py # 这个是事件处理的，主要逻辑在这个里面书写
│  m_singledb.py #这个是数据库类
│  README.MD #说明文件
│  Server.py # socket主文件
│  Utils.py # 功能文件
│  __init__.py
```

### 使用

用户开发只需要关注`Config.py`，`Api.py` ，`Events.py`

### Config.py

里面设置一些配置参数（包括运行端口，数据库账号密码，API路由等），用户可以自己加，不做过多说明

### Api.py

这是使用tornado.websocket的一个优点，它可以同时监听http服务，所有就使访问websocket内部提供了一个简洁的方法，可以为空实现

#### 例如添加一个获取在线人数的api

首先在config里面引入相关控制器，并定义路由

```python
from GMWebSockets.Api import *
# route
sec_route = [
    (r"/status", StatusHandler)
]
```

接着在Api里面实现改控制器

```
import tornado.ioloop
import tornado.web
from tornado.escape import json_encode
from GMWebSockets.Utils import *

class StatusHandler(tornado.web.RequestHandler):
    def get(self):
        global allsockets
        online_num = len(allsockets.keys())
        self.finish({'online_num': online_num})
```

由于这个py可以访问其他文件的所有参数，结合tornado.web开发，实现的功能可以有非常多种

### Events.py

这里是websocket主文件，主要需要用户实现`onConnet`，`onMessage`，`onClose`的方法

#### 先来清楚一些概念

allsockets（dict）：储存所有socket的数组

socket_id（int）：每个连接的唯一id，通过id可以找到对应的socket对象，完成数据发送

alllclients（dict）：存储auth过的用户，会存储一个client_id指向socket_id

clinet_id（int）：自定义的一个client_id，需要前端自己绑定，从而实现快捷的发送消息

allgroups（dict）：存储一个用户分组

group_id（str）：有时候我们需要进行分组广播，可以自定义一个group_id（组的名称）

心跳默认是15秒一个，如果3次前端都没有应答，就关闭这个连接，超时时间 = time_out_interval*time_out_times

当一个socket连接过来，如果auth_timeout秒内没有发起auth,bind，就会被中断连接

### 方法

> 所有方法细节，可以在Utils里面查看

#### write_message
直接使用sokcet给自己发送消息

```
socket.write_message(message)
```

#### send_to_all，send_to_all_sockets

给所有sokcet 发送消息，不管有没有验证

```
send_to_all(message)
send_to_all_sockets(message)
```

#### send_to_all_clients

给所有client发送消息,只有绑定了才发

```
 send_to_all_clients(message):
```

#### send_to_socket

给单个socket 发送消息

```
send_to_socket(socket_id,message)
```

#### send_to_client

给单个用户发送消息

```
send_to_client(client_id,message)
```

#### join_group
将用户加入一个组

```
join_group(client_id,group_id)
```

#### leave_group
将用户踢出一个组

```
leave_group(client_id, group_id)
```

#### get_clientcount_bygroup
获取某个组的人数

```
get_clientcount_bygroup(group_id)
```

#### send_to_group
向某个组广播消息

```
send_to_group(group_id, message)
```

#### is_socket_id_online
判断socket 是否在线

```
is_socket_id_online(socket_id)
```

#### is_client_id_online
判断某个用户是否在线

```
is_client_id_online(client_id)
```

#### set_session ,update_session
设置一个seesion 这个建议直接用socket.属性，去设置保留参数

```
set_session(socket_id,session)
```

#### get_session
获取seesion 这个建议直接用socket.属性，去设置保留参数

```
get_session(socket_id)
```

### 案例

注意：前端只能发送json格式数据，data里面的键值可以自己根据需求定义

```
{"type":"bind","data":{"client_id":1}}
```

当前端发送send_all时候，给所有人广播

前端

```json
{"type":"send_to_all","data":{"message":"hello all"}}
```

后端

```python
    def onMessage(socket,json_data):
        global allclients,allsockets

        type = json_data['type']
        data = json_data['data']
        
        if type == "send_to_all":
            socket_id = str(socket.socket_id)
            if not hasattr(socket,'client_id'):
                client_id = "<not bind>"
            else:
                client_id = str(socket.client_id)
            message = "socket_id:" + socket_id + "client_id:" + client_id + "send to all :" + data['message']
            return send_to_all(message)        
```



## 后续计划

- [ ] 升级为RFC6455协议
- [ ] 实现多进程程协同
- [ ] 引入apscheduler模块
- [ ] 其他



如果该项目能帮到你，欢迎star

如果对该项目有什么建议，欢迎issue，pr