import queue
import threading

# 内置的queue模块实现了多生产者、多消费者队列，且其中的几种队列类型中的操作都实现了锁原语，所以它们是线程安全的
# 原语：由若干个机器指令构成的完成某种特定功能的一段程序，具有不可分割性；即原语的执行必须是连续的，在执行过程中不允许被中断。
# queue模块下的几种队列类型的区别仅在于元素被取出的顺序:
# queue.Queue(maxsize=0) (FIFO-先进先出队列)
# Queue用到了双端队列（collection.deque），双端队列的操作是原子性的
# queue.LifoQueue(maxsize=0) (LIFO-后进先出队列，类似于堆栈)
#   上述两种的元素可以是任何对象
# queue.PriorityQueue(maxsize=0) (优先级队列，优先级高的先返回)
#   优先级队列的元素应是一个二元组-(priority_number, data)，
#   优先级的高低：对队列中的二元组进行升序排序（先比较priority的值，如果相同，则比较data），越小的优先级越高
#   如果data没有可比性，那数据将封装为dataclass对象，仅比较优先级数字
# queue.SimpleQueue() (无界的FIFO队列，简单的队列，没有任务跟踪等高级功能)

q = queue.Queue(maxsize=20)


def worker():
    while True:
        item = q.get()
        print(f"{item} 处理中...")
        print(f"{item} 处理完毕。")
        q.task_done()   # 调用task_done()告诉队列前一个取出的数据已经处理完毕了


def product():
    for i in range(30):
        q.put(i)
    print("所有任务已添加。")


thread_worker = threading.Thread(target=worker, daemon=True)
# 如果不设置消费者线程为daemon，那么join解除阻塞后，该线程还是会因为get()而被阻塞
# 当join解除阻塞后，消费者线程应该随之终止，所以应该设置守护线程
thread_product = threading.Thread(target=product)
thread_worker.start()
thread_product.start()
q.join()  # 主线程调用join()，所以这里会阻塞主线程，直到队列的所有任务被处理
print("所有任务处理完毕。")


# join():
# put()成功添加一个元素，未完成任务计数加一
# 调用task_done()一次，表示取出的任务处理完毕，则未完成任务计数减一
# 当未完成任务计数为0时，结束对调用join()的线程的阻塞
