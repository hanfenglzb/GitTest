import threading
import time

# 全局变量
# 同一个进程下的所有线程共享进程中的资源，所以全局变量可以被所有线程访问和修改，这样就可以实现线程间的通信。
# 但是如果线程对共享变量的操作不是原子性的话，就可能造成线程不安全。
# 通过线程同步原语，例如Lock、RLock、Condition等，也可以保证线程安全。
# 对于一般的生产者-消费者模型，queue模块已经实现好了，平时开发的时候直接使用queue模块即可，
# 不需要再通过共享变量+各种同步原语的方式实现。


DATA = []


def get_data(data):
    for i in range(20):
        data.append(i)


def parse_data(data):
    while True:
        try:
            item = data.pop()
        except IndexError:
            pass
        else:
            time.sleep(0.5)
            print(item)
            break


thread_get = threading.Thread(target=get_data, args=(DATA,))
thread_get.start()
thread_get.join()
# 同时开启20条线程，因为没有锁定，所以是线程不安全的
for _ in range(len(DATA)):
    thread_parse = threading.Thread(target=parse_data, args=(DATA,))
    thread_parse.start()
if len(DATA):
    thread_parse.join()
