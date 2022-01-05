import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9999))

while True:
    client.send(input("[input]: ").encode("gbk"))
    bytes_data = client.recv(1024)
    str_data = bytes_data.decode("gbk")
    print(f"{str_data}")
