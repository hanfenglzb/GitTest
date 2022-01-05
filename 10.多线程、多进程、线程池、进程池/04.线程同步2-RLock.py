import threading

# RLock-重入锁（递归锁）
# RLock和Lock的区别并不大，只是多了"递归等级"和"所属线程"的概念，其他都是类似的
# 递归等级：一个线程获得重入锁，同一个线程再次获取它不会被阻塞
# 所属线程：重入锁被锁定后，就归属于这个线程，只有这个线程能够解锁它

# acquire(blocking=True, timeout=-1)
# 类似于Lock的acquire方法，只是当一个线程获得锁后，将归属于这个线程，只有这个线程可以解锁它，
# 当这个线程再次尝试获得锁，不会被阻塞，当然其他线程还是会被阻塞。
# 一个线程获得一次锁，自增递归等级（从0开始，0个递归等级代表这个锁没有被锁定，不属于任何一个线程）
# 调用一次acquire获得锁一次，就返回一次True，否则会被阻塞。
# 而blocking为False或阻塞时间超过timeout，调用acquire会返回False，表示该线程没有获得锁，
# 但不影响该线程后续代码的运行，只是没有锁的保护可能造成线程的不安全。

# release()
# 释放锁，自减递归等级。只有最后一次release()，将递归等级减到0才真正释放锁，
# 也就是一个线程acquire几次就得release几次，必须成对出现，否则还是会造成死锁。
# 只有获得锁的线程才能释放锁。当锁被真正释放后，如果有多个线程被阻塞等待这个锁解锁，只有一个线程能解除阻塞继续运行。


lock = threading.Lock()
r_lock = threading.RLock()


# 一、不小心写错
def func():
    lock.acquire()
    print("t1二次获得锁被阻塞")
    lock.acquire()
    # 在没有释放的二次获得锁造成阻塞，会形成死锁
    print("t1解锁lock")
    lock.release()


t1 = threading.Thread(target=func)
t1.start()
print("主线程解锁lock")
lock.release()


# 二、线程函数的部分逻辑抽离成一个函数，在这个函数里面为了保证线程同步，也使用了同一个锁
# 为什么抽离的函数中也要加锁？
# 抽离出来的代码如果也使用这个临界资源，这部分代码不知道会在什么时候被哪个线程调用，如果不加锁，
# 万一正在使用的时候线程被切换了，其他线程就能正常使用这个资源，忽视锁的存在，那就造成线程不安全了。
# 这是很常见的使用场景，逻辑上没有错，但是会造成在没有解锁的时候二次锁定，导致线程被阻塞，造成死锁
# 这个时候抽离出的函数可以使用另外的锁，也可以使用重入锁解决。
def func1():
    global lock
    lock.acquire()
    ...
    # do_something
    do_sth()
    lock.release()


def do_sth():
    global lock
    lock.acquire()
    ...
    lock.release()


t2 = threading.Thread(target=func1)
# t2.start()


# 使用重入锁解决上述的死锁
def func2():
    r_lock.acquire()
    # do_something
    do_sth1()
    r_lock.release()


def do_sth1():
    r_lock.acquire()
    ...
    r_lock.release()


t3 = threading.Thread(target=func2)
t3.start()
