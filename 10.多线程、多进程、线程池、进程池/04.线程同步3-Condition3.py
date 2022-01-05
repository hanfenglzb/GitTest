import threading
import time


# 生产者-消费者模型
# 生产商品数量达到一定条件后被消费
class Produce(threading.Thread):
    """生产者，生产5个产品后等待消费"""
    def __init__(self, name, product_num):
        super().__init__(name=name)
        self.product_num = product_num

    def run(self):
        global num
        with condition:
            while True:
                if num >= self.product_num:
                    print(f"{self.name}: 已有{self.product_num}个产品，停止生产")
                    condition.notify()  # 通知消费者可以消费了
                    condition.wait()    # 等待消费
                else:
                    num += 1
                    print(f"{self.name}: 产品数[{num}]")
                    time.sleep(wait_time)


class Consume(threading.Thread):
    def __init__(self, name, money):
        super().__init__(name=name)
        self.money = money

    def run(self):
        global num
        with condition:
            while self.money:
                if num <= 0:
                    print(f"{self.name}: 没货了，通知生产者")
                    condition.notify()  # 通知生产者开始生产
                    condition.wait()    # 等待生产者通知可以消费了
                else:
                    self.money -= 1
                    num -= 1
                    print(f"{self.name}: 消费了1个产品，剩余{num}个")
                    time.sleep(wait_time)
        print(f"{self.name}: 没钱了，停止消费")


if __name__ == '__main__':
    print("Condition: produce-consume-num".center(30, "-"))
    condition = threading.Condition()
    num = 0
    wait_time = 0.5
    producer = Produce("生产者", 5)
    producer.daemon = True
    consumer1 = Consume("消费者1", 10)
    consumer2 = Consume("消费者2", 5)
    consumer3 = Consume("消费者3", 10)
    consumer4 = Consume("消费者4", 5)
    producer.start()
    consumer1.start()
    consumer2.start()
    consumer3.start()
    consumer4.start()
