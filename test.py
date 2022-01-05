from abc import ABC, abstractmethod


# 工厂方法
class AbstractFactory(ABC):
    @abstractmethod
    def factory_method(self):
        pass

    def show(self):
        product = self.factory_method()
        product.produce()


class HorseFactory(AbstractFactory):
    def __init__(self, color, weight):
        self.color = color
        self.weight = weight

    def factory_method(self):
        print("养马场正在生产马...")
        return Horse(
            color=self.color,
            weight=self.weight
        )


class Animal(ABC):
    @abstractmethod
    def produce(self):
        pass


class Horse(Animal):
    def __init__(self, color, weight):
        self.color = color
        self.weight = weight

    def produce(self):
        print(f"生产了一匹颜色为{self.color}，体重为{self.weight}kg的马。")


HorseFactory("red", 200).show()


# 单例
class MetaSingleton(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super().__call__(*args, **kwargs)
        return cls._instance[cls]


class Singleton(metaclass=MetaSingleton):
    pass


print(Singleton() is Singleton())


def singleton_decorator(cls):
    cls._instance = {}

    def wrapper(*args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = cls(*args, **kwargs)
        return cls._instance[cls]

    return wrapper


@singleton_decorator
class Singleton(object):
    pass


print(Singleton() is Singleton())


# 策略模式
class Context(object):
    def __init__(self, strategy):
        self.strategy = strategy

    def show(self):
        print(f"选择了{type(self.strategy).__name__}策略。")
        self.strategy.show()


class AbstractStrategy(ABC):
    @abstractmethod
    def route_recommend(self):  # 路线推荐
        pass

    @abstractmethod
    def show(self):
        pass


class DriveStrategy(AbstractStrategy):
    def route_recommend(self):
        print("推荐开车方式前往")

    def show(self):
        print("开车的路线是...")


class WalkStrategy(AbstractStrategy):
    def route_recommend(self):
        print("推荐走路方式前往")

    def show(self):
        print("走路的路线是...")


walk_strategy = WalkStrategy()
context = Context(strategy=walk_strategy)
context.show()
