import socket
from urllib.parse import urlparse
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ


selector = DefaultSelector()
stop_flag = False


class Fetcher(object):
    def __init__(self, url):
        self.host = None
        self.path = None
        self.client = None
        self.data = b""
        self.url = url
        self.get_url()

    def get_url(self):
        url = urlparse(self.url)
        self.host = url.netloc
        self.path = url.path
        if not self.path:
            self.path = "/"

    def close_client(self):
        self.client.close()

    def create_client(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(False)
        try:
            self.client.connect((self.host, 80))
        except BlockingIOError:
            pass
        # 注册事件-client的文件描述符、写事件、回调函数callback_send
        # 当该文件描述符的写事件准备好，执行回调函数
        selector.register(self.client.fileno(), EVENT_WRITE, self.callback_send)

    def send(self):
        self.client.send(
            f"GET {self.path} HTTP/1.1\r\nHost:{self.host}\r\nConnection:close\r\n\r\n".encode("utf-8")
        )

    def recv(self):
        dat = self.client.recv(1024)
        if dat:
            self.data += dat
            return True
        return False

    def callback_send(self, key):
        global selector
        # 取消该事件的注册
        selector.unregister(key.fd)
        self.send()
        # 注册事件-client文件描述符、读事件、回调函数callback_recv
        selector.register(self.client.fileno(), EVENT_READ, self.callback_recv)

    def callback_recv(self, key):
        global selector
        continue_recv = self.recv()
        if not continue_recv:
            selector.unregister(key.fd)
            self.data = self.data.decode("utf-8")
            print(self.data)
            self.close_client()

    def get(self):
        self.create_client()


def event_loop():
    # 事件循环，不停的请求socket的状态并调用回调函数
    while True:
        try:
            for key, mask in selector.select():
                callback_func = key.data
                callback_func(key)
        except OSError:
            break


if __name__ == '__main__':
    fetcher = Fetcher(url="https://www.baidu.com/")
    fetcher.get()
    event_loop()
