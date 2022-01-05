import threading
import time


# 单一生产者-单一消费者模型
# 生产者生产产品，当产品生产成功后通知消费者使用产品，消费者使用完产品后通知生产者继续生产产品
def produce():
    global product
    count = 1
    with condition:
        while count <= 10:
            if product is None:
                print(f"{threading.current_thread().name}: 开始生产产品")
                time.sleep(wait_time)
                product = f"袜子-{count}"
                count += 1
                print(f"{threading.current_thread().name}: 已生产产品[{product}]")
                condition.notify()  # 通知消费者
                condition.wait()    # 等待消费
            else:
                condition.wait()    # 等待消费


def consume():
    global product
    with condition:
        while producer.is_alive():
            if product is not None:
                print(f"{threading.current_thread().name}: 开始消费产品")
                time.sleep(wait_time)
                print(f"{threading.current_thread().name}: 卖出产品[{product}]")
                product = None
                condition.notify()  # 通知生产者消费完成
                condition.wait()    # 没有产品，等待生产
            else:
                condition.wait()    # 没有产品，等待生产


if __name__ == '__main__':
    print("Condition: produce-consume".center(30, "-"))
    product = None
    wait_time = 0.1
    condition = threading.Condition()
    producer = threading.Thread(target=produce, name="producer")
    consumer = threading.Thread(target=consume, name="consumer")
    # consumer = threading.Thread(target=consume, name="consumer", daemon=True)
    producer.start()
    consumer.start()
    producer.join()
    # 当消费完最后一个产品，生产线程解除阻塞，但是消费者线程还在等待生产线程的通知，造成堵塞
    # 消费者线程要么是守护线程，要么需要condition再通知一次，解除消费者的阻塞
    with condition:
        condition.notify()

