import threading


# Timer-定时器对象
# 一个操作应该在等待一定的时间之后运行
# Timer是Thread的子类，所以可以跟一个自定义线程一样操作
# class threading.Timer(interval, function, args=None, kwargs=None)
#   在经过interval的时间间隔后，执行function，位置参数用args，关键字参数用kwargs

# cancel
# 停止计时器，并取消本应该执行的function。只能在仍处于等待时间时取消。

def func():
    print("execute func")


timer = threading.Timer(5, func)
timer.start()
if input("cancel?(Y/N)") in ("Y", "Yes", "YES"):
    timer.cancel()


# 自定义timer的实现
class Timer(threading.Thread):
    def __init__(self, interval, function, args=None, kwargs=None):
        threading.Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args if args is not None else ()
        self.kwargs = kwargs if args is not None else {}
        self.finished = threading.Event()

    def cancel(self):
        self.finished.set()  # 将内置标识设置为True

    def run(self):
        self.finished.wait(self.interval)   # 阻塞self.interval秒
        if not self.finished.is_set():  # 阻塞时间过后，如果标识为False，说明没有被取消
            self.function(*self.args, **self.kwargs)
        self.finished.set()  # 设置标识为True




