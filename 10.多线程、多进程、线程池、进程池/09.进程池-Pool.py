import multiprocessing as mp
import time


# 进程池的用法跟ProcessPoolExecutor差不多，方法有一些区别：

# class Pool(processes=None, initializer=None, initargs=(), maxtasksperchild=None, context=None)
# processes:
#   进程池的最大进程数，不指定的情况下设置为 os.cpu_count() or 1
# initializer:
#   每个进程在开始运行前先执行的函数
# initargs:
#   initializer函数对象的参数
# maxtasksperchild:
#   一个工作进程最多执行的任务数。
#   一般情况下，进程池中的工作进程开启后，会运行死循环，不断的从队列中获取任务执行，不会执行完一个任务就死亡，
#   即开启后的工作进程会一直运行直到进程池被关闭，然后才终止死亡。也就是该参数为None的情况。
#   但是如果设置了这个参数，那么在一个进程完成了这个参数指定的这么多的任务之后，会终止该进程，清理、释放资源，
#   然后启动一个新的进程代替旧的工作进程。
# context: 进程上下文

#


def get_html(index):
    time.sleep(index)
    print(f"{mp.current_process().name}")
    print(f"get page{index} success")
    return index


if __name__ == '__main__':
    pool = mp.Pool(processes=5)
    pool.apply_async()