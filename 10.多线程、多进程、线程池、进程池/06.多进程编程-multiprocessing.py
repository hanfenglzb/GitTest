import multiprocessing as mp
import os


# multiprocessing和threading基本相似，包括Process类、各种锁等等，
# 多了Pool-线程池、Queue-进程安全队列、Pipe-管道、Manager-管理器、共享内存和其他一些模块函数等

# multiprocessing模块中常用的一些模块方法
# active_children()
#   返回当前进程存活的子进程的列表。
#   调用该方法会清理已经死亡的进程资源（即清理僵尸进程）
# cpu_count()
#   返回系统CPU数量。如果无法获取，抛出NotImplementedError
#   当前可用的CPU数量：len(os.sched_getaffinity(0))
# current_process()
#   返回当前进程对象-Process对象
# parent_process()
#   返回当前进程的父进程对象。如果当期进程是主进程，返回None
# freeze_support()
# get_all_start_methods()
# get_context(method=None)
# get_start_method(allow_none=False)
# set_executable()
# set_start_method(method)


# 使用多进程的第一种方式：Process实例化
# class multiprocessing.Process(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)
# 类似于Thread()
# group:
#   暂无意义
# target:
#   由run()方法调用的可调用对象，表示进程应该执行的任务，默认为None，表示进程不做什么事
# name:
#   显示指定进程名称，用于识别进程，没有语义，进程名可以是一样的，一般在调用start()之前要设置好名称。
#   默认为None:
#       如果不主动设置，则会被自动命名为"Process-N"，其中N为该进程的第几个子进程
# args和kwargs:
#   target参数传递的可调用对象的参数传递方式
# daemon:
#   设置进程为守护进程（True/False），调用start()之后就不能设置了。默认为None，继承父进程的daemon属性

# Process类的一些方法和属性
#   run()/start()/join()/is_active()/name/daemon等属性和方法和Thread()类似
# 其他属性和方法:
# pid(ident):
#   返回进程id，如果进程未启动，返回None
# exitcode:
#   进程退出状态码，如果进程还没有终止，返回None
#   0: 正常终止
#   N:
#   -N: N表示进程是被信号N终止的
# authkey:
#   进程身份验证字节串-bytes，一般只有网络编程会用到该验证字节串。
#   主进程使用通过os.urandom()随机产生的一个32字节串；子进程未设置该属性时继承父进程的属性
#   这个键的用途是为涉及网络连接的底层进程间通信提供安全性，这类连接只有在具有相同的身份验证键时才能成功。
# sentinel:
#   系统对象的数字handler，当进程结束时将变为 "ready"
#   windows上为操作系统handler；linux上为文件描述符
# terminate()
#   立即终止进程。如果被终止的进程有子进程，那么所有子进程都会变成孤儿进程（包括守护进程）。
#   windows上使用TerminateProcess()，unix上使用SIGTERM信号
# kill()
#   立即终止进程。unix上使用SIGKILL信号。
# terminate和kill终止的进程不会变成僵尸进程，操作系统会回收资源（因为是发送信号终止的）
# 但是，强行终止一个进程，如果这个进程有使用Pipe、Queue，有可能造成它们被损坏，其他进程用不了。
# 如果进程已经获得锁、信号量这些，终止后资源被释放，可能造成其他进程的死锁。
# 所以，强行终止进程应该保证不会影响其他进程或程序。
# close()
#   关闭Process对象，释放Process对象持有的所有资源。
#   如果进程还在运行，或者还有子进程在运行，则不能关闭，抛出ValueError。
c = 0


def add(a, b=0):
    print(a + b)
    print("c", c)
    print(f"进程ID: 1-{mp.current_process().pid} 2-{os.getpid()}")
    print(f"父进程ID: {os.getppid()}")
    print(f"进程名: {mp.current_process().name}")
    print(f"进程身份验证字符串: {mp.current_process().authkey}")
    return a + b


# 如果子类重写了__init__()，要保证在做任何事之前先调用Process的__init__()，进行Process的初始化
class MyProcess(mp.Process):
    def __init__(self, func, args=(), kwargs=None):
        super().__init__()
        self.res = None
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.res = self.func(*self.args, **self.kwargs)

    def get_res(self):
        return self.res
        # while Ture:
        #     if self.res:
        #         return self.res


if __name__ == '__main__':
    # 创建进程的三种方式：
    #   spawn:
    #       启动新的解释器进程，子进程只会复制运行run()方法所必须的资源。创建进程的速度比以下两种方式慢
    #   fork:
    #       父进程使用os.fork()分叉出一条子进程，子进程会复制父进程启动它时的所有资源和状态。
    #       如果父进程是多线程进程，会很麻烦，需要考虑的事情就多了。
    #   forserver:
    #       类似于fork。启动服务器进程，父进程需要启动子进程时访问服务器进程并请求它分叉出一条子进程。
    #       服务器进程是单现场进程。
    # 如何设置启动方式？
    # mp.set_start_method("spawn or fork or forkserver")
    # 在windows上只能设置spawn模式

    # Process的实例化
    print("实例化方式".center(20, "-"))
    process1 = mp.Process(target=add, args=(1,), kwargs={"b": 2})
    process2 = mp.Process(target=add, args=(2,), kwargs={"b": 3})
    process1.start()
    process2.start()
    process1.join()
    process2.join()
    print("继承方式".center(20, "-"))
    my_process = MyProcess(add, args=(2,), kwargs={"b": 3})
    my_process.start()
    my_process.join()
    print(my_process.exitcode)
    # 注意：各个进程之间的内存都是独立的，这就意味着一个进程的变量在另一个进程是不能直接获取到的，
    # 比如下面在父进程中想要获取my_process对象中的res属性，本意是想要获取子进程中的运行结果，
    # 但是，它在父进程中访问这个进程对象，这个进程对象处于父进程的内存中，是属于父进程的！
    # 并没有真正访问到子进程中的这个值！
    # 所以，获取进程的返回值不能跟线程一样，必须使用进程间的通信方式-Queue、Pipe、Manager、shared-memory等
    print(my_process.res)  # None
