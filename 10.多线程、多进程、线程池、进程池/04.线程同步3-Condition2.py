import threading
import time


# 单一生产者-多消费者模型
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
                with condition1:
                    condition1.notify()  # 通知消费者
                condition.wait()  # 等待消费
            else:
                condition.wait()  # 等待消费


def consume():
    global product
    with condition1:
        while producer.is_alive():
            if product is not None:
                print(f"{threading.current_thread().name}: 开始消费产品")
                time.sleep(wait_time)
                print(f"{threading.current_thread().name}: 卖出产品[{product}]")
                product = None
                with condition:
                    condition.notify()  # 通知生产者消费完成
                condition1.wait()  # 没有产品，等待生产
            else:
                condition1.wait()  # 没有产品，等待生产


if __name__ == '__main__':
    print("Condition: produce-consume".center(30, "-"))
    product = None
    wait_time = 0.1
    condition = threading.Condition()
    condition1 = threading.Condition()
    producer = threading.Thread(target=produce, name="producer")
    consumer = threading.Thread(target=consume, name="consumer")
    consumer1 = threading.Thread(target=consume, name="consumer1")
    producer.start()
    consumer.start()
    consumer1.start()
    producer.join()
    with condition1:
        condition1.notify_all()
