import threading


# Condition-条件变量
# 用于复杂的线程同步；当一个线程需要等待（阻塞状态）其他线程中的一些条件发生，当在某个线程中条件达到了，
# 就可以通知等待的线程（解除阻塞），让它接着运行。
# 条件变量通常与一个锁相关联。
# 需要在多个条件变量中共享一个锁时，可以传递一个Lock/RLock锁给构造方法，否则他将自己产生一个RLock锁。

# acquire()
#   请求底层锁
# release()
#   释放底层锁
# wait(timeout) 必须在获得底层锁下运行。
#   挂起线程timeout秒(为None时一直阻塞)，直到收到notify通知或者超时才会被唤醒继续运行。
#   原理：调用wait()首先会判断是否获得了底层锁，如果没有获得，则抛出RuntimeError，如果已经获得底层锁，
#   则新生成一个Lock锁并锁定它，将新生成的锁添加进内部维护的双端队列中，然后释放底层锁，再调用这个新锁锁定它一次，
#   使线程阻塞。等某个线程调用notify()唤醒该线程后，它又重新获得底层锁，继续线程后续的运行。
# wait：释放底层锁，生成新锁添加进队列，阻塞线程，然后等待唤醒，重新获得底层锁

# notify(n=1)  必须在获得底层锁下运行。
#   通知挂起的线程开始运行，默认通知正在等待该condition的线程，可同时唤醒n个（按wait调用顺序）。
#   原理：调用notify不会释放底层锁，但会释放调用wait()生成的锁，唤醒被阻塞的线程。
# notify：从队列中获取锁并释放该锁，按队列添加顺序释放锁，所以wait的线程也被按顺序释放锁，但是释放后谁先被调度运行就不一定了

# notifyAll() 必须在获得底层锁下运行。
#   通知所有被挂起的线程开始运行。


# 条件变量示例1：
# 假设有小爱同学和天猫精灵进行对话
# 天猫精灵：小爱同学
# 小爱同学：在
# 天猫精灵：我们来对古诗吧
# 小爱同学：好啊
# 天猫精灵：我住长江头
# 小爱同学：君住长江尾
# 天猫精灵：日日思君不见君
# 小爱同学：共饮长江水
# 天猫精灵：此水几时休
# 小爱同学：此恨何时已
# 天猫精灵：只愿君心似我心
# 小爱同学：定不负相思意


# 使用原始锁对象
class TianMao(threading.Thread):
    def __init__(self, name, _lock):
        super().__init__(name=name)
        self.lock = _lock

    def run(self):
        self.lock.acquire()
        print(f"{self.name}: 小爱同学")
        self.lock.release()

        self.lock.acquire()
        print(f"{self.name}: 我们来对古诗吧")
        self.lock.release()


class XiaoAi(threading.Thread):
    def __init__(self, name, _lock):
        super().__init__(name=name)
        self.lock = _lock

    def run(self):
        self.lock.acquire()
        print(f"{self.name}: 在")
        self.lock.release()

        self.lock.acquire()
        print(f"{self.name}: 好啊")
        self.lock.release()


# 使用Condition条件变量
class TianMao2(threading.Thread):
    def __init__(self, name, cond):
        super().__init__(name=name)
        self.condition = cond

    def run(self):
        with self.condition:
            for word in t_lst:
                print(f"{self.name}: {word}")
                self.condition.notify()  # 通知小爱同学线程解除阻塞
                self.condition.wait()  # 阻塞，等待小爱同学线程的通知


class XiaoAi2(threading.Thread):
    def __init__(self, name, cond):
        super().__init__(name=name)
        self.condition = cond

    def run(self):
        # self.condition.acquire()
        with self.condition:
            for word in x_lst:
                self.condition.wait()  # 阻塞，等待天猫精灵线程的通知
                print(f"{self.name}: {word}")
                self.condition.notify()  # 通知天猫精灵线程解除阻塞
        # self.condition.release()


if __name__ == '__main__':
    t_lst = ["小爱同学", "我们来对古诗吧", "我住长江头", "日日思君不见君", "此水几时休", "只愿君心似我心"]
    x_lst = ["在", "好啊", "君住长江尾", "共饮长江水", "此恨何时已", "定不负相思意"]
    print("Lock".center(20, "-"))
    lock = threading.Lock()
    t1 = TianMao("天猫精灵", lock)
    x1 = XiaoAi("小爱同学", lock)
    t1.start()
    x1.start()
    t1.join()
    x1.join()
    # 正常的逻辑应该是天猫精灵运行输出一句，然后阻塞，轮到小爱同学运行回答，等待小爱同学的回答。
    # 但是只有单一锁的话，首先天猫精灵获得锁（因为线程先启动）运行，这个时候天猫精灵甚至能把所有代码都运行完，
    # 然后再轮到小爱同学。
    print("Condition".center(20, "-"))
    condition = threading.Condition()
    t2 = TianMao2("天猫精灵", condition)
    x2 = XiaoAi2("小爱同学", condition)
    # 注意，小爱同学要先启动，否则天猫精灵启动执行，发出通知后进行等待，这时小爱同学还没有启动，通知无效。
    # 等小爱同学启动，也在等待天猫精灵的通知，两者相互等待造成死锁。
    x2.start()
    t2.start()
    t2.join()
    x2.join()
    # 小爱同学启动
    #   获取底层锁，然后调用wait()，释放底层锁，生成新锁，调用两次后阻塞小爱同学，此时还处于wait方法中；
    # 切换到天猫精灵
    #   获取底层锁，输出"天猫精灵"，调用notify()，释放小爱同学的新锁，解除小爱同学的阻塞，然后调用wait()，
    #   释放底层锁，生成天猫精灵的新锁，阻塞天猫精灵；
    # 切换到小爱同学
    #   继续wait()的运行，获取底层锁，输出"在"，调用notify()，释放天猫精灵的新锁，解除其阻塞状态，
    #   然后调用wait()，释放底层锁，生成小爱同学的新锁，阻塞小爱同学；
    # 切换到天猫精灵
    #   继续wait()的运行，获取底层锁，输出"我们来对古诗吧"，调用notify()，释放小爱同学的新锁，解除其阻塞状态，
    #   然后调用wait()，释放底层锁，生成天猫精灵的新锁，阻塞天猫精灵；
    # 以此类推...
