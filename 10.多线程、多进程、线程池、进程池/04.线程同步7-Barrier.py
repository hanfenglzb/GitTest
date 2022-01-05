import threading
import time


# Barrier-障碍锁（栅栏锁）
# 固定数量的线程需要相互等待，直到这些线程都准备好。
# 就相当于路上有一个道闸，只有道闸前等待的人数到达指定数量，才会开闸放行。
# 放行之后道闸将再次关闭，进行新一轮的等待。所以使用障碍锁的线程数必须是障碍锁指定放行数的倍数，
# 否则最后一次开闸后再次等待开闸的线程将一直处于等待状态。

# class threading.Barrier(parties, action=None, timeout=None)
# parties: 开闸放行所需的线程数
# action: 函数对象，每次开闸放行后将由其中一个等待的线程释放前被调用
#   如果该函数调用后抛出异常，会使栅栏进入破损状态
# timeout: 栅栏对象的默认超时时间

# 属性及方法
# wait(timeout=None)
# 在没有到达指定的线程数时，所有调用它的线程将被阻塞，等待放行（包括最后一个调用的）。
# 当等待的线程数达到指定数量后，开闸放行。
# 只要调用了wait()，不管后面就会返回一个id值（0到[parties - 1]，根据调用的先后顺序）
# timeout：
#   如果指定了timeout，则使用指定的，否则使用栅栏对象创建时的默认超时时间。
#   如果被阻塞的线程发生超时，会使栅栏进入破损状态

# reset()
# 重置栅栏为默认的初始态，使栅栏重新可用；如果重置时仍有线程在等待，那么这些线程会引发BrokenBarrierError

# abort()
# 使栅栏进入破损状态

# parties
# 栅栏放行的线程数量

# n_waiting
# 当前时刻正在栅栏前阻塞的线程数量

# broken
# 表示栅栏是否处于破损状态-True/False

# threading.BrokenBarrierError
# 如果栅栏处于破损状态，那么所有已经调用了wait()或后续调用wait()的线程都将抛出BrokenBarrierError
#   1.调用action时抛出异常，栅栏损坏
#   2.调用wait()时发生超时，栅栏损坏
#   3.调用abort()主动损坏栅栏
# 如果重置栅栏时，还有线程在等待放行，那么这些线程会抛出BrokenBarrierError
# 这很好理解，栅栏已经被损坏了，不能再起到一个拦截线程的作用，这些线程要么在抛出BrokenBarrierError后终止运行
# 要么主动捕获它，定义当出现这种情况后应该怎么处理


# 达到指定人数后开门放行
class WaitOpen(threading.Thread):
    def __init__(self, name, _barrier):
        super().__init__(name=name)
        self.barrier = _barrier

    def run(self):
        n_waiting = self.barrier.n_waiting
        parties = self.barrier.parties
        print(f"{self.name}: 等待开门...目前有{n_waiting + 1}个人在等，还差{parties - n_waiting - 1}个")
        bid = self.barrier.wait()
        print(f"{self.name}: 门开了，go go go，我的编号是{bid}")


class WaitOpen1(threading.Thread):
    def __init__(self, name, _barrier):
        super().__init__(name=name)
        self.barrier = _barrier

    def run(self):
        while True:
            print(f"{self.name}: 等待开门...")
            try:
                bid = self.barrier.wait()
            except threading.BrokenBarrierError:
                print(f"{self.name}: 真晦气！我就不走，我接着等！")
            else:
                print(f"{self.name}: 门开了，go go go，我的编号是{bid}")
                break


class Manager(threading.Thread):
    def __init__(self, name, _barrier):
        super().__init__(name=name)
        self.barrier = _barrier

    def run(self):
        print(f"{self.name}: 走走走，这次不开门!")
        self.barrier.reset()


class WaitOpen2(threading.Thread):
    def __init__(self, name, _barrier):
        super().__init__(name=name)
        self.barrier = _barrier

    def run(self):
        if not self.barrier.broken:
            print(f"{self.name}: 等待开门...")
        try:
            bid = self.barrier.wait()
        except threading.BrokenBarrierError:
            print(f"{self.name}: 门被人拆了！")
        else:
            print(f"{self.name}: 门开了，go go go，我的编号是{bid}")


class Destroyer(threading.Thread):
    def __init__(self, name, _barrier):
        super().__init__(name=name)
        self.barrier = _barrier

    def run(self):
        print(f"{self.name}: 什么破门，看我拆了它!")
        self.barrier.abort()


if __name__ == '__main__':
    def action():
        print(f"{threading.current_thread().name}: 人数够了，开门！")


    barrier = threading.Barrier(3, action)
    for thread_name in "ABCDEF":
        t = WaitOpen(thread_name, barrier)
        t.start()
    time.sleep(3)
    print("-" * 20)
    t1 = WaitOpen1("1", barrier)
    t2 = WaitOpen1("2", barrier)
    t3 = WaitOpen1("3", barrier)
    manager = Manager("manager", barrier)
    t1.start()
    t2.start()
    manager.start()
    t3.start()
    time.sleep(3)
    print("-" * 20)
    t1 = WaitOpen2("a", barrier)
    t2 = WaitOpen2("b", barrier)
    t3 = WaitOpen2("c", barrier)
    destroyer = Destroyer("destroyer", barrier)
    t1.start()
    t2.start()
    destroyer.start()
    t3.start()
