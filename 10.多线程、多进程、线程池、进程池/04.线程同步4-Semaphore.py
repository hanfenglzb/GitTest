import random
import threading
import time


# Semaphore-信号量
# 限制并发的线程数量，同一时间最多只能有指定数量的线程访问共享资源，其他线程处于等待状态。
# 内部实现使用一个条件变量，根据计数器的值wait()或notify()，实现线程的阻塞和运行。
# 信号量管理一个内部计数器（默认的初始计数为1），
# 线程需要读取关联信号量的共享资源时，需调用acquire()，这时信号量的计数器会-1
# 线程不需要共享资源时，需调用release()，这时信号量的计数器会+1，处于等待队列最前面的线程会先释放锁被唤醒，
# 但是也不能保证是它先被调度
# 信号量控制规则：
#   当计数器大于等于1时，可以为线程分配共享资源权限；
#   当计数器为0时，没有访问权限的线程阻塞并加入等待队列，直到其他线程释放权限

# acquire(blocking=True, timeout=None)
# 如果是阻塞模式：
#   如果计数器的值大于等于1，则计数器值减1
#   如果计数器的值等于0，则调用条件变量的wait()，阻塞当前线程

# release(n=1)
# n要大于等于1的整数
# 计数器的值增加n，然后解除n个阻塞的线程
# 这就会造成问题：
#   假如有一个计数为3的信号量，有10个线程，同一时间只能有3个线程并发，其他的7个线程将被阻塞。
#   调用3次acquire()，此时计数器减至0，然后在一个线程执行完或者结束访问共享变量，调用release(n=5)，将计数器的值增加到5，
#   这会使有5个线程可以运行，那么这个时候并发的线程数就有7个了，违背了信号量的原意。
# 当n不为1时，会导致计数器的值超过初始值，释放次数过多。
# 所以一个信号量最好是一个线程acquire()了num次，那么就要release()num次（或者release(n=num)）

# BoundedSemaphore-有界信号量
# 有界信号量就是解决计数器的值可能超过初始值的问题，当计数器的值超过初始值时，会抛出ValueError，
# 也就是说，信号量被锁定多少次，就只能释放多少次。有界信号量能减少信号量的释放次数多于其请求次数的错误。
# 例子：一个数据库同一时间只允许n个连接
# semaphore = Semaphore(value=n)
# def work():
#     semaphore.acquire()
#     conn = connect_db()
#     try:
#         # ... use connection ...
#     finally:
#         conn.close()
#     semaphore.release(2) # 不小心释放了2次
# 那后面连接数据库的线程就会超过n个了
# bounded_semaphore = BoundedSemaphore(value=n)
# def work():
#     with bounded_semaphore:
#         with connect_db() as conn:
#             # ... use connection ...
# 其实使用with语法，Semaphore也不会有问题，就是在单独调用acquire()和release()时，不小心释放多了，
# 面对这种有限资源的情况，就可能会出现问题。


# 示例：控制线程的并发
class HtmlSpider(threading.Thread):
    def __init__(self, name, url, _semaphore):
        super().__init__(name=name)
        self.semaphore = _semaphore
        self.url = url

    def run(self):
        time.sleep(1)
        print(f"{self.name}: get html success!")
        self.semaphore.release()    # 线程运行完毕，释放一个信号量，让出位置给其他线程运行


class UrlProducer(threading.Thread):
    def __init__(self, name, _semaphore):
        super().__init__(name=name)
        self.semaphore = _semaphore

    def run(self):
        print(f"{self.name}: url提取完毕")
        for i in range(20):
            # 锁定信号量，减少一个计数，当运行3次for循环后（3个线程开始运行），被阻塞，直到计数器值大于等于1
            self.semaphore.acquire()
            url = f"https://www.baidu.com/pages/{i}"
            html_thread = HtmlSpider(f"html_thread{i}", url, self.semaphore)
            html_thread.start()


# 信号量实现同步
class Producer(threading.Thread):
    def __init__(self, name, _semaphore):
        super().__init__(name=name)
        self.semaphore = _semaphore

    def run(self):
        global item
        time.sleep(1)
        item = random.randint(0, 100)
        print(f"{self.name}: {item}")
        self.semaphore.release()    # 信号量计数加1


class Consumer(threading.Thread):
    def __init__(self, name, _semaphore):
        super().__init__(name=name)
        self.semaphore = _semaphore

    def run(self):
        global item
        print(f"{self.name}: 等待producer运行...")
        # 如果有多个消费者线程，那么producer只会release一次，只有一个消费者线程能解除阻塞运行
        self.semaphore.acquire()    # 信号量计数减1，等待producer的释放
        print(f"{self.name}: {item}")


if __name__ == '__main__':
    semaphore = threading.Semaphore(3)  # 创建一个信号量，计数器值设为3
    url_thread = UrlProducer("url_thread", semaphore)
    url_thread.start()
    url_thread.join()
    print("produce-consume".center(20, "-"))
    semaphore1 = threading.Semaphore(0)
    item = 0
    producer = Producer("producer", semaphore1)
    consumer = Consumer("consumer", semaphore1)
    consumer2 = Consumer("consumer2", semaphore1)
    consumer.start()
    consumer2.start()
    producer.start()
