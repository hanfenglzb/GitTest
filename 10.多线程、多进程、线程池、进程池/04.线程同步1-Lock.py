import threading
import dis
import time


def add(a):
    a += 1


print(dis.dis(add))

# 临界资源：同一时间只能被一个线程访问的共享资源
# 临界区：访问临界资源的代码段
# 当有任意数量的线程都可以访问临界区的代码时，为了保证同一时间只能有一个线程访问临界区，就需要保证线程的同步
# 线程的同步可以选择合适的同步原语实现，也可以通过线程的控制机制实现
#   线程控制机制：
#       CPython中GIL的存在使同一时间只能有一个线程运行，但是如果线程中关于操作临界区的操作不是一个原子性操作的话，那么线程是不安全的
#       可以通过join()，sleep()等方法使阻塞其他线程，保证当前线程访问的同步
#   同步原语：
#       线程的控制机制也不能保证同步的绝对正确，而且阻塞的释放时机是不好把握的，这个时候可以选择合适的同步原语实现线程同步

# Python中的同步原语包括：
#   Lock-原始锁
#   RLock-可重入锁（递归锁）
#   Semaphore-信号量
#   Condition-条件变量
#   Event-事件锁
#   Barrier-障碍锁（栅栏锁、屏障锁）


# Lock-原始锁
# 原始锁是一个在锁定时不属于特定的某个线程的同步基元组件。
#   也就是说，在没有锁定时，任何一个线程都能尝试锁定它，而锁定后任何一个线程中都能将它解锁。
# 原始锁有锁定（locked/状态为True）和非锁定状态（unlocked/状态为False），在刚创建时处于非锁定状态。

# 下列所有方法的执行都是原子性的。
# acquire(blocking=True, timeout=-1)
# 阻塞或非阻塞的获得锁
#   当Lock处于非锁定状态时，调用它会将Lock改为锁定状态，并返回True，表示该线程获得了锁
#   当Lock处于锁定状态时，调用它将阻塞尝试锁定它的线程，直到在某个线程中调用了release()将它解锁了，
#       才会解除对这个线程的阻塞，并在调度到它运行时重新将锁锁定，返回True，表示这个线程获得了锁
#   blocking：设为False的话，调用它的时候如果锁已经处于锁定状态下将不再阻塞线程，并直接返回False，表示没有获得锁。
#   timeout：设置为正值调用时，只要无法获得锁，将最多阻塞 timeout 设定的秒数
#       在timeout期间，如果获得锁那么返回True，否则timeout后将不再阻塞线程，并直接返回False，表示没有获得锁
# 非阻塞模式下或超时后，没有获得锁的线程其运行不受影响，只是可能造成线程不安全。
# 所以原始锁一般使用阻塞模式实现<互斥锁>，所有线程都按这个模式，就能保证线程安全

# release()
# 释放一个锁。这个方法可以在任何线程中调用释放被锁定的锁，不单指获得锁的线程。
# 如果有其他线程在等待这个锁解锁而处于阻塞状态，那么调用它只会解除其中一个线程的阻塞状态。
# 释放未锁定的锁会引发RuntimeError
# 该方法没有返回值

lock = threading.Lock()


def func():
    global num  # 全局变量
    # lock.acquire()  # 获得锁，加锁
    num1 = num
    time.sleep(1)  # 阻塞1s，否则一个线程被调度的时候足够运行完这些代码
    num = num1 - 1
    # lock.release()  # 释放锁，解锁


num = 100
lst = []
for i in range(100):  # 开启100个线程
    t = threading.Thread(target=func)
    t.start()
    lst.append(t)
# 等待线程运行结束
for i in lst:
    i.join()

print(num)


# 没有获得锁的情况下，开启100个线程，此时所有线程都处于就绪状态，当第一个线程被调度后运行，获取到全局的num值后，
# 碰到等待1s的操作，该线程被阻塞，这个时候该线程不再参与调度，而1s已经足够让所有线程都竞争到GIL运行一遍了，
# 这样所有的线程获取到的num值都会是100，每个线程的运算结果都是99，所以最终的全局num值是99。
# 如果等待的时间足够小，则有可能有的线程获得的全局num值是其他线程计算过后的值
# （有的线程在sleep过后再一次参与调度，且比没运行过的线程先被调度运行，那么全局num的值就会被改变）

# 如果加上锁，那么第一个被调度的线程获得锁，碰到sleep被阻塞，让出CPU，第二个被调度的线程尝试获得锁，
# 但是发现该锁已经是锁定状态，所以也被阻塞，调度到其他线程运行的时候同理，全都被阻塞。只有当第一个获得锁的线程经过0.1s后解除了阻塞，
# 再次运行，全局num值-1，直到在该线程中释放这个锁之后，其他被阻塞的线程中的一个解除阻塞，重新进入就绪状态，等待被解释器进程调度。
# 所以即使获得锁的线程在没有释放锁的时候被切换了，也可以阻塞掉其他尝试获得这个锁的线程，直到获得这个锁的线程再次运行去释放掉这个锁，
# 其他线程才能再次去获得这个锁。这样在牺牲了性能的情况下，保证数据安全。

# Lock锁和GIL锁的区别：
# Lock锁：它是为了保护共享的数据，同时刻只能有一个线程来修改共享的数据，而保护不同的数据需要使用不同的锁。
# GIL锁：限制一个解释器进程中同一时刻只有一个线程被调度，GIL锁是解释器级别的锁，高于Lock锁。
# Lock锁和GIL锁同时存在：
# 同时存在两个线程A、B，A、B中都有同一个Lock
# A先被调度，在A中对Lock进行锁定，但并未运行结束就被切换了
# 此后B先被调度，在B中也对Lock进行锁定，但发现已经被A锁定，且还没有解锁，则B被阻塞，
# 当A再一次被调度，执行完操作，并对Lock进行解锁，解除B的阻塞，然后A被切换
# 当B再被调度时，才能对Lock进行锁定，正常运行。

# 死锁
# 线程竞争有限的资源时，互相锁定，都要求对方先进行解锁，就会造成死锁
# 第一种常见情况
def func():
    global lock
    lock.acquire()
    lock.acquire()
    print("重复锁定2次")
    lock.release()


t = threading.Thread(target=func)
t.start()
t.join()
# 一个锁在没有解锁的时候再次锁定，这就造成第二次锁定的线程被阻塞，形成死锁


# 第二种常见情况
lock1 = threading.Lock()
lock2 = threading.Lock()


def func1():
    lock1.acquire()
    print(f"{threading.current_thread().name}锁定lock1")
    time.sleep(1)  # 阻塞线程A一秒
    lock2.acquire()
    print(f"{threading.current_thread().name}锁定lock2")
    lock2.release()
    print(f"{threading.current_thread().name}解锁lock2")
    lock1.release()
    print(f"{threading.current_thread().name}解锁lock1")


def func2():
    lock2.acquire()
    print(f"{threading.current_thread().name}锁定lock2")
    time.sleep(1)  # 阻塞线程B一秒
    lock1.acquire()
    print(f"{threading.current_thread().name}锁定lock1")
    lock1.release()
    print(f"{threading.current_thread().name}解锁lock1")
    lock2.release()
    print(f"{threading.current_thread().name}解锁lock2")


t1 = threading.Thread(target=func1, name="thread-A")
t2 = threading.Thread(target=func2, name="thread-B")
t1.start()
t2.start()
# 线程A先被调度，锁定了lock1，然后阻塞1s。在这1s的过程中，线程B被调度，锁定了lock2，然后阻塞1s。
# 在线程B阻塞1s的时候，线程A结束1s的阻塞再次被调度，想要锁定lock2，但是lock2已经线程B锁定，线程A被阻塞，等待lock2被释放。
# 线程B结束1s的阻塞再次被调度，想要锁定lock1，但是lock1已经被线程A锁定，线程B被阻塞，等待lock1被释放。
# 线程A、B都想要获得对方锁定的锁，导致出现死锁。
