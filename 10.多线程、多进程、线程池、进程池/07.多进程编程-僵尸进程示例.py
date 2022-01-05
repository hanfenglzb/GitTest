import time
import multiprocessing as mp


def zombie():
    print(mp.current_process().name)
    print(mp.current_process().pid)
    time.sleep(10)


if __name__ == '__main__':
    # 孤儿进程
    for i in range(10):
        process = mp.Process(target=zombie, name=f"zombie_process{i}")
        process.start()
    time.sleep(100)
    # start子进程之后，主进程等待100s，不进行任何操作，也就不会自动清理，所以子进程结束后全部变成僵尸进程，
    # 孤儿进程会被系统进程收养并且通知操作系统回收资源
