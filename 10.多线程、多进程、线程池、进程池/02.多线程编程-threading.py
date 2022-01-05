import threading

# Python的多线程目前没有优先级、线程组的概念，线程还不能被销毁、停止、暂停、恢复或中断
# 一个Python进程会自动创建一个主线程，主线程和其他线程一样，如果没有被其他进程阻塞，它也是正常运行然后终止。
# 主线程的终止并不代表程序退出，如果还有其他的非守护线程，程序会等其他的非守护线程终止后才退出。
# 一个线程中抛出异常，会导致线程终止，但并不影响其他线程，除非其他线程都是守护线程。

# 守护线程：当只剩下守护线程时，程序将直接退出。
# 可以通过Thread(..., daemon=True)或Thread().daemon = True设置一个线程为守护线程。
# 这个值只能在线程对象调用start()前设置，否则将抛出RunTimeError。
# 如果没有设置（默认为None），那么将继承创建该线程的父线程的daemon属性；
# 主线程是非守护线程，所以通过主线程创建的线程，默认都是非守护线程。
# 主线程的终止并不代表程序的终止，还要看是否有其他的非守护线程存活。
# 如果程序中没有非守护线程，守护线程将被直接关闭，这个时候可能造成守护线程中的资源没有正确释放（例如打开的文件对象等）

# 线程阻塞
# 如果线程不阻塞，那么不管是守护线程还是非守护线程，都会一直运行，直到终止。
# Thread().join(timeout=None)
# 调用线程对象的join方法，将导致该线程的父线程在调用join()处被阻塞
# timeout：超时时间，可选参数，以秒为单位
#   如果为None（默认），父线程被阻塞直到线程子线程终结；
#   如果为一个正浮点数（负数会被当成0），父线程被阻塞直到发生超时（如果到达超时时间前子线程已经终结，则父线程不再阻塞，继续向后运行）
# 子线程可以多次调用join()阻塞父线程，而父线程也可以被不同的子线程阻塞。
# join()总是返回None，如果要判断一个线程是否发生超时需要调用is_alive()判断该线程其是否还存活
# 如果还存活，说明线程的运行时间超过了timeout，则肯定发生了超时

# Thread().start()
# 开始线程活动。只能被调用一次，后续将调用run()

# Thread().run()
# run()方法从开始执行到执行结束的期间代表线程是活动（alive）的。
# 标准的run()方法会发起对target参数中的可调用对象的调用，会从Thread()的args参数和kwargs参数
# 分别获取可调用对象的位置参数和关键字参数

# 使用多线程的两种方式
# 1.通过threading.Thread类的实例化
# Thread(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=False)
# group
# 目前没有意义，为以后扩展ThreadGroup线程组类而预留的参数。默认为None
# target
# 用于run()方法的可调用对象。默认为None，表示这个线程不需要调用任何方法
# name
# 显示指定线程名称。用于识别线程，没有语义，线程名可以是一样的，一般在调用start()之前要设置好名称，
# 默认为None
#   如果没有指定target参数，则线程会被命名为"Thread-N"(N为整数)，主线程固定为：MainThread
#   如果指定了target参数，则线程会被命名为"Thread-N (target.__name__)"
# args和kwargs
# 如果target参数传递的可调用对象有参数，可以通过这两个参数传递，args是位置参数形式，kwargs是关键字参数形式
# daemon
# 设置线程是否为守护线程（False/True）
# 默认为None，则线程会继承父线程的daemon属性
# 线程start()之后不能再设置


def add(a, b=0):
    print(a + b)


thread_demo = threading.Thread(target=add, args=(1,), kwargs=dict(b=1))
print(thread_demo.name, thread_demo.daemon)
thread_demo.name = "thread_demo"
thread_demo.daemon = True
print(thread_demo.name, thread_demo.daemon)
thread_demo.start()
print(thread_demo.name)
thread_demo.join()


# 2.通过继承Thread类
# 继承Thread类
# 这里要注意，如果子类重载了__init__()，那么一定要保证在重载的__init__()做任何事之前，
# 先发起对Thread类的__init__()的调用：
# 1.super().__init__(): 一般简单的单重继承可以用super，如果是多重继承或是多继承，最好还是显示调用更好。
# 2.Thread.__init__(self): 显示通过Thread显示调用__init__
# 如果线程函数有返回值，就可以通过继承的方式，重写run()，获取返回值
class MyThread(threading.Thread):
    def __init__(self, func=None, args=()):
        super().__init__()
        self.func = func
        self.args = args
        self._res = None

    def run(self):
        self._res = self.func(*self.args)

    def get_res(self):
        return self._res
        # while True:
        #     if self._res:
        #         break
        # return self._res


def sub(a, b):
    return a - b


thread_demo1 = MyThread(func=sub, args=(1, 2))
thread_demo1.start()
thread_demo1.join()     # 需要等待线程结束后获取返回值
print(thread_demo1.get_res())
