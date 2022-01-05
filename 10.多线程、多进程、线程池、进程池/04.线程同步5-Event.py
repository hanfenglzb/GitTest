import threading


# Event-事件对象
# 一个线程发出事件信号，而其他线程等待该信号的发生。
# 内部实现还是条件变量
# 事件对象维护一个内部标识（True/False），如果这个标识为False，
# 那么所有调用wait()的线程将阻塞，直到标识被改变为True。
# 事件对象刚创建时内部标识为False

# set()
# 将内部标识设置为True，并notify_all()，解除所有阻塞的线程
# clear()
# 将内部标识设置False
# wait(timeout=None)
# 如果调用时内部标识为False，那么将阻塞线程，直到内部标识被改变为Ture，并返回False
#    非阻塞状态则超时后返回False
# 如果调用时内部标识为True，那么将不阻塞线程，并直接返回True
# is_set()
# 返回内部标识

# 一个处理线程需要等待另一个线程完成初始化工作
class Process(threading.Thread):
    def __init__(self, name, _event):
        super().__init__(name=name)
        self.event = _event

    def run(self):
        print(f"{self.name}: Wait for initialization to complete")
        self.event.wait()
        self.event.clear()  # 重置标识
        print(f"{self.name}: start processing...")


class Initial(threading.Thread):
    def __init__(self, name, _event):
        super().__init__(name=name)
        self.event = _event

    def run(self):
        print(f"{self.name}: initializing")
        self.event.set()


if __name__ == '__main__':
    event = threading.Event()
    # 处理线程等待初始化工作完成
    process = Process("process", event)
    initial = Initial("initial", event)
    process.start()
    initial.start()
