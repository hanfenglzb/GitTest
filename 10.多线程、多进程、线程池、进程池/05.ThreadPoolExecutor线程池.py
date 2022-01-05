import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, FIRST_COMPLETED


# >>>线程池/进程池<<<
# 为什么要使用线程池/进程池？
# 1.控制同一时间并发的线程数/进程数
# 2.可以获取线程/进程的状态及返回值
# 3.当一个线程/进程运行结束，主线程/进程可以立即知道
# 4.通过Executor抽象基类，统一线程池、进程池的接口

# >>>Executor-抽象基类<<<
# 提供异步执行的接口方法，统一线程池和进程池的实现

# >>>ThreadPoolExecutor-线程池<<<
#   Executor的子类，使用线程池异步执行调用；

# ThreadPoolExecutor(max_workers=None, thread_name_prefix='', initializer=None, initargs=())
# 参数：
# max_workers: 线程池在异步执行调用的时候最大可用的线程数
#   即线程池的最大任务（可调用对象）并发数。
#   线程池中线程的创建时间：
#       一个任务通过submit()提交后，会创建一个future对象，然后将这个future对象和任务函数，
#       还有其他的一些参数封装成一个work_item提交到一个队列中，然后看是否有空闲的线程。
#       如果没有，则看已经创建的线程数是否超过了max_workers，没有则新建一个线程（也是threading.Thread创建）
#       从队列中获取这个刚添加的work_item去执行，否则这个work_item一直处于队列中，等待有线程运行完上一个任务，
#       然后再从队列中获取它执行。
#       work_item被调用之后，会在其中调用任务函数，并得到它的结果（或捕获到异常）设置到future对象中。
#       而线程池中的线程则会执行一个while True循环，不断的从队列中获取work_item执行。
#       当线程被创建后，除非线程池被关闭，否则是不会死亡的。
#   max_workers为None时，开启的线程数为min(32, os.cpu_count() + 4) - python3.8+

# thread_name_prefix: 线程池的线程名字前缀
# 默认情况下线程池的线程命名为: f"ThreadPoolExecutor-{线程池数（从0开始）}_{线程数（从0开始）}"
# 给了该参数: f"{thread_name_prefix}_{线程数（从0开始）}"
# 用于调试，可查看某个任务是由哪个线程池的哪个线程执行的

# initializer: 传递一个可调用对象，当线程池中的每一条线程第一次创建并启动时调用它。
# initargs：如果initializer有参数，通过它传递（元组形式）
# 如果initializer抛出了异常，所有已提交或后面提交给线程池的任务都会抛出BrokenThreadPool异常

# 方法：
# submit(fn, /, *args, **kwargs)
# 向线程池提交任务，等待线程池的调度运行，并立即返回一个Future对象
# 如果fn有参数，以*args，**kwargs的方式传递

# map(func, *iterables, timeout=None, chunksize=1)
# 将iterables中的每个元素作为参数传递给func，异步运行func(生成len(iterables)个future对象)，
# 返回一个生成器，生成的值为各个future的返回值。类似于内置的map()函数，func有几个参数就需要几个iterables，
# 除了以下两点；
#   iterables是立即执行而不是延迟执行的；内置的map会在迭代返回的生成器时才逐个执行。
#   func是异步执行的，对func的多个调用可以并发执行。但是func的返回值还是按iterables原有的顺序生成。
# timeout：
#   迭代返回的生成器获取future的返回值时(调用__next__逐个获取)，当碰到一个future还没执行完成，
#   获取不到返回值，就看是否还在timeout之内（从调用map开始算），没超时就阻塞，等待它运行完成后获取返回值，
#   如果发生超时就会抛出concurrent.futures.TimeoutError。
#   也就是说在timeout时间内，所有任务要完成，否则就会抛出TimeoutError
#   timeout为None的话会一直阻塞，直到所有。
# chunksize在ThreadPoolExecutor中无效
# 如果执行func时抛出异常，那么在使用这个返回的生成器时，也会抛出同样的异常。

# shutdown(wait=True, *, cancel_futures=False)
# 关闭线程池，释放所有分配给线程池的资源
# 关闭线程池后，再调用submit和map就会抛出RuntimeError，也就是调用该方法后不能再提交任务给线程池
# wait：
#   True：阻塞，直到已经提交给线程池的所有任务完成，释放已分配的资源
#   False：不阻塞，但是也会完成所有已经提交的任务，释放已分配的资源
# cancel_futures:
#   Ture: 取消所有还未开始执行的任务，但是已经完成或正在运行的不会被取消
#   False: 不取消

# 使用线程池后需要关闭
# with语法
# with ThreadPoolExecutor(max_workers=4) as executor:
#     ...
# 等价于：
# executor = ThreadPoolExecutor(max_workers=4)
# ...
# executor.shutdown()

# >>>ProcessPoolExecutor-进程池<<<
# 进程池的方法和逻辑和线程池差不多是一样的。这里待深究......

# >>>Future-未来对象<<<
# 将可调用对象封装为异步执行。
# 它的实例应该由submit方法创建，而不应该在代码中显示的创建，除非是进行测试。
# 任务提交后生成的future对象会添加进一个队列，等待线程或进程的执行。通过future对象，可以获取任务的执行情况，执行结果等信息。
# future的几个状态：
#   PENDING-待处理的
#   RUNNING-运行中
#   FINISHED-结束运行
#   CANCELLED-被用户取消的
#   CANCELLED_AND_NOTIFIED-被内部取消的[_Worker.add_cancelled()]

# 任务指提交的可调用对象，每个任务都会返回一个future对象
# cancel()
# 尝试取消运行已提交的任务。
# 如果任务正在运行或已经运行完成，则不能被取消，返回False
# 如果任务还没有开始运行则取消任务的运行，或已经被取消了，返回True

# cancelled()
# 如果任务成功被取消，返回True，否则返回False

# running()
# 如果任务正在运行，返回True，否则返回False

# done()
# 如果任务已被取消或正常运行结束，返回True，否则返回False

# result(timeout=None)
# 返回任务的返回值。
# timeout：如果任务还在运行，那么将等待timeout秒，超时后抛出concurrent.futures.TimeoutError
# 如果为None，则阻塞直到任务完成，获取到返回值
# 如果任务被取消了，再调用result会抛出concurrent.futures._base.CancelledError
# 任务运行时抛出一个异常，则该方法也会抛出同样的异常

# exception(timeout=None)
# 返回任务运行时抛出的异常，如果任务正常完成，则返回None
# timeout：如果任务还在运行，那么将等待timeout秒，超时后抛出concurrent.futures.TimeoutError
# 如果为None，则阻塞直到任务抛出异常或正常完成。
# 如果任务被取消了，再调用exception会抛出concurrent.futures._base.CancelledError

# add_done_callback(fn)
# 给future对象添加一个回调函数，当任务被取消或者正常完成后，调用它。
# 如果添加这个函数的时候，任务已经被取消或已经完成，则立即调用。
# 这个回调函数只能有一个参数，当被调用时，future对象作为它的参数传入。
# 该回调函数中引发的异常是Exception的子类，将被忽略；是BaseException的子类，行为没有定义，该抛异常就抛。
# 可以添加多个回调函数，按添加的顺序调用。

# ... 其他几个测试方法


# >>>as_completed<<<
# 提交由已有的future对象构成的迭代对象，返回一个生成器对象，生成的值是已经完成(或已经取消)的future对象。
# 如果提交的时候future对象已经是完成状态(或已经被取消)，那么会优先作为生成值，后续谁先完成谁就先生成。
# 这里的future对象可以是由不同的线程池submit的（future对象一般只由submit返回）。
# timeout：
#   迭代返回的生成器获取已完成的future对象时(调用__next__逐个获取)，如果碰到不能成功的获取
#   下一个已完成的future对象，就看是否还在timeout时间内(从调用as_completed开始计算)，
#   没超时就阻塞，直到成功获取已完成的future对象，已超时就抛出concurrent.futures.TimeoutError。
#   也就是说在timeout时间内，所有的future都要完成，否则就会抛出TimeoutError。
#   timeout为None时，会一直阻塞，直到所有future完成。

# map和as_completed的对比：
# 都是立即返回一个生成器；
#   map生成的值是已完成的future.result()
#   as_completed生成的值是已完成的future。
# 生成值的顺序不同：
#   map是按给的iterables元素的顺序生成future，并且也按这个顺序生成值
#   as_completed是哪个future先完成，就先生成哪个future。
# future对象不同：
#   下面的Executor指它的子类：ThreadPoolExecutor/ProcessPoolExecutor
#   map是Executor的方法，所有的future都是由同一个Executor生成，
#       并且在调用map的时候future还没有生成，由map自己根据提供的func和iterables生成
#   as_completed是futures包的函数，不管是哪个Executor生成的future都可以，
#       并且在调用as_completed的时候future已经生成了，甚至有可能都已经执行完了。

# >>>wait<<<
# 提交由已有的future对象构成的迭代对象，返回一个由集合构成的namedtuple二元组(DoneAndNotDoneFutures)
# DoneAndNotDoneFutures(done={<Future at 0x255db7333a0 state=finished returned int>},
# not_done={<Future at 0x255db733220 state=running>, <Future at 0x255db722c40 state=running>})
# 元组的第一个元素为done，包含已经完成或被取消的future对象
# 元组的第二个元素为not_done，包含正在运行或未开始运行的future对象
# timeout: 控制返回前的最大等待秒数，为None则不限制等待时间
# return_when: 函数在什么时候返回（阻塞到什么时候）
#   FIRST_COMPLETED: 在提交的future对象出现一个已经运行结束或被取消的时候返回；
#   FIRST_EXCEPTION: 在提交的future对象中出现一个抛出异常的时候返回；如果都没有抛出异常，就跟ALL_COMPLETED一样
#   ALL_COMPLETED: 在提交的future对象都已经运行结束或被取消的时候返回；
# timeout和return_when同时指定时，timeout优先，timeout结束，直接返回。

# 初级用法
def get_html(index):
    time.sleep(index)
    print(f"{threading.current_thread().name}")
    print(f"get page{index} success")
    return index


print("original".center(20, "-"))
executor = ThreadPoolExecutor(1)  # 创建线程池
future1 = executor.submit(get_html, 1)  # 提交任务并立即返回一个future
future2 = executor.submit(get_html, 2)
future3 = executor.submit(get_html, 3)
for task in [future1, future2, future3]:
    print(task.result())
executor.shutdown()     # 关闭线程池


# 使用as_completed()
print("as_completed".center(20, "-"))
executor = ThreadPoolExecutor(3)
all_futures = [executor.submit(get_html, page_num) for page_num in [3, 2, 4]]
for future in as_completed(all_futures):
    res = future.result()
    print(res)
executor.shutdown()  # 阻塞直到executor资源释放

# 使用Executor.map()
print("Executor.map".center(20, "-"))
executor = ThreadPoolExecutor(3)
for res in executor.map(get_html, [3, 2, 4]):
    print(res)
executor.shutdown()  # 阻塞直到executor资源释放

# 使用wait()
print("wait".center(20, "-"))
executor = ThreadPoolExecutor(1)
all_futures = [executor.submit(get_html, page_num) for page_num in [3, 2, 4]]
all_futures[1].cancel()
wait_res = wait(all_futures, return_when=FIRST_COMPLETED)
print(wait_res)
print("main_thread")
executor.shutdown()  # 阻塞直到executor资源释放
