# 给每个socket用户分配一个唯一id
allsockets={}
# 分配一个client_id对应表
allclients={}
# 分配一个groupdict
allgroups={}
# 在线人数
online_num = 0

# 给所有sokcet 发送消息，不管有没有验证
def send_to_all(message):
    global allsockets
    for user in allsockets.values():
        user.write_message(message)

# 给所有sokcet 发送消息，不管有没有验证
def send_to_all_sockets(message):
    global allsockets
    for user in allsockets.values():
        user.write_message(message)

# 给所有client发送消息,只有绑定了才发
def send_to_all_clients(message):
    global allsockets
    for user in allsockets.values():
        if user.client_id:
            user.write_message(message)

# 给单个socket 发送消息
def send_to_socket(socket_id,message):
    global allsockets
    allsockets[socket_id].write_message(message)

# 给单个用户发送消息
def send_to_client(client_id,message):
    global allsockets
    global allclients
    allsockets[allclients[client_id]].write_message(message)

# 将用户加入一个组
def join_group(client_id,group_id):
    global allgroups
    if not hasattr(allgroups,group_id):
        allgroups[group_id]=[client_id]
    else:
        allgroups[group_id].append(client_id)

# 将用户踢出一个组
def leave_group(client_id, group_id):
    global allgroups
    if not hasattr(allgroups,group_id):
        allgroups[group_id].pop(client_id)
        if len(allgroups)==0:
            del allgroups[group_id]
    else:
        return

# 获取某个组的人数
def get_clientcount_bygroup(group_id):
    global allgroups
    if not hasattr(allgroups,group_id):
        return len(allgroups[group_id])
    else:
        return 0

# 向某个组广播消息
def send_to_group(group_id, message):
    global allgroups
    if not hasattr(allgroups,group_id):
        return
    for socket in allgroups[group_id]:
        socket.write_message(message)

# 判断socket 是否在线
def is_socket_id_online(socket_id):
    global allsockets
    for socket in allsockets.keys():
        if socket == socket_id:
            return True
    return False

# 判断某个用户是否在线
def is_client_id_online(client_id):
    global allclients
    for client in allclients.keys():
        if client == client_id:
            return True
    return False

# 绑定一个用户id
def bind_clinet_id(socket_id,clinet_id):
    global allclients,allsockets
    allclients[clinet_id] = socket_id
    allsockets[socket_id].client_id = clinet_id

# 设置一个seesion 这个建议直接用socket.属性，去设置保留参数
def set_session(socket_id,session):
    global allsockets
    allsockets[socket_id].session = session

# 更新一个seesion 这个建议直接用socket.属性，去设置保留参数
def update_session(socket_id,session):
    global allsockets
    allsockets[socket_id].session = session

# 获取seesion 这个建议直接用socket.属性，去设置保留参数
def get_session(socket_id):
    global allsockets
    return allsockets[socket_id].session