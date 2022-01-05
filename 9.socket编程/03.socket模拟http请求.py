import socket
from urllib.parse import urlparse


def get_url(url):
    # 解析url
    url = urlparse(url)
    host = url.netloc   # 域名
    path = url.path     # 路径
    print(f"url: {url} 域名：{host} 路径：{path}")
    if not path:
        path = "/"
    # 建立socket连接
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, 80))
    client.send(
        f"GET {path} HTTP/1.1\r\nHost:{host}\r\nConnection:close\r\n\r\n".encode("utf-8")
    )
    data = b""
    while True:
        dat = client.recv(1024)
        if not dat:
            break
        data += dat
    data = data.decode("utf-8").split("\r\n\r\n")[1]
    print(data)
    client.close()


get_url("http://www.baidu.com/")

