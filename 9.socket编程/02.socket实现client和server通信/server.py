import socket
import threading

# 服务端：
# 创建：server = socket.socket(协议, 类型, ...)
# 绑定：server.bind((ip, port))
#   ip地址和port是服务端的
# 监听：server.listen()
# 建立连接：sock, r_address = server.accept()
#   sock：服务端创建的新socket对象，用于和客户端连接通信
#   r_address：建立连接的远端地址，一个二元组，包括ip和port
# 发送：sock.send(bytes)
# 接收：bytes = sock.recv(bufsize)
#   bufsize：一次从缓冲区读取的数据长度

# 客户端：
# 创建：client = socket.socket(协议, 类型, ...)
# 建立连接：client.connect((服务器端的ip或域名, 服务器端的port))
# 发送：client.send(bytes)
# 接收：bytes = client.recv(bufsize)


# 该socket对象用于监听连接
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 9999))      # 绑定主机IP和端口
server.listen()     # 正式监听绑定的IP和端口


def haddle_sock(sock, addr):
    while True:
        bytes_data = sock.recv(1024)
        # 得到bytes数据，需要根据编码解码
        # 假如客户端使用的是gbk编码
        str_data = bytes_data.decode("gbk")
        print(f"[ip:{addr[0]} port:{addr[1]}]: {str_data}")
        sock.send(input("[input]: ").encode("gbk"))


def accept():
    while True:
        sock, r_addr = server.accept()  # 如果监听到socket连接请求，生成新的socket对象，用于和客户端通信
        client_thread = threading.Thread(target=haddle_sock, args=(sock, r_addr))
        client_thread.start()


client_accept = threading.Thread(target=accept, name="client_accept")
client_accept.start()
