import time
import multiprocessing as mp


def sub(a, b):
    print(a - b)


def add(a, b):
    print(a + b)
    try:
        mp.Process(target=sub, args=(a, b)).start()
    except AssertionError as e:
        print(e)
        # 守护进程不允许再创建子进程
    time.sleep(2)
    print(a, b)


if __name__ == '__main__':
    # 守护进程
    process = mp.Process(target=add, args=(2, 3), daemon=True)
    process.start()
    time.sleep(1)
    # start子进程之后，主进程等待1s，子进程输出a+b，然后等待2s，1s后主进程退出，
    # 因为子进程是守护进程，所以被被强制终止了，不会执行下一个输出
