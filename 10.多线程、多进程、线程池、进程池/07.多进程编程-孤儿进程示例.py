import time
import multiprocessing as mp


def add(a, b):
    print(a + b)
    time.sleep(2)
    print(a, b)


if __name__ == '__main__':
    # 孤儿进程
    process = mp.Process(target=add, args=(2, 3))
    process.start()
    # start子进程之后，主进程退出，子进程还在等待2s，所以非守护进程的子进程变成了孤儿进程
    # 孤儿进程会被系统进程收养并且通知操作系统回收资源
