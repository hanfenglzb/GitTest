# 接口类(Interface)
# 接口是对象公开方法的一种集合，在Java中通常以interface关键字来定义
# 接口实现过程和类相似，但是具有不同的概念，主要有以下几点不同之处：
# 1.类实现了对象的属性和方法，接口只对使用该接口需要实现的方法进行定义，没有具体实现
# 2.类可以实例化，接口不可以被实例化
# 3.类中的方法可以是实现，接口中的方法都是抽象方法
# 抽象方法（纯虚函数）：抽象方法的概念是父类中只负责声明该方法，但不具体实现这个方法，实现部分由继承该类的子类负责实现

# 抽象类(Abstract Base Class)
# 抽象类型(abstract types)是指一类不可直接实例化，只可被继承的类。对应的，能够直接实例化的类称作具体类型(concrete types)。
# 在Python中，抽象类是以抽象基类的形式来实现的，抽象基类的英文为：abstract base classes（ABC）
# 通常在抽象基类中会定义一些抽象方法或抽象属性。继承于抽象基类的子类必须给出所有抽象方法和属性的具体实现，才可以进行正常的实例化。
# 在面向对象思想中，抽象基类一般用于统一接口，使得业务代码可以不随着实现得改变而改变（因为抽象基类已经确定了接口）
# 优点：
# 1.处理继承问题方面更加规范、系统
# 2.明确调用之间的相互关系
# 3.使得继承层次更加清晰
# 4.限定子类实现的方法
# 抽象类和接口类概念相近，但有一些不同的地方
# 1.继承接口的子类需要实现接口中指定的所有抽象方法；但抽象基类没有这么严格的要求
# 2.接口要求所有方法都是抽象方法；而抽象基类中可以有抽象方法，也可以有已经实现的方法

# 1.抽象类是一个介于类和接口之间的概念，同时具备类和接口的部分特性，可以用来实现归一化设计
# 2.在继承抽象类的过程中，应该尽量避免多继承；而在继承接口的时候，反而鼓励多继承接口
# 一般情况下单继承能实现的功能都是一样的，所以在父类中可以有一些简单的基础实现
# 而多继承的情况由于功能比较复杂，所以不容易抽象出相同的功能的具体实现来写在父类中
# java里的所有类的继承都是单继承，所以抽象类完美的解决了单继承需求中的规范问题
# 但对于多继承的需求，由于java本身语法的不支持，所以创建了接口Interface这个概念来解决多继承的规范问题
# python中只支持抽象类没有接口类，但因为python支持多继承，所以也可以用抽象类多继承去模拟出接口类


# 抽象基类的特点：
# 1.可以定义抽象方法，也可以定义具体的实现方法
# 2.至少要定义一个抽象方法；没有定义抽象方法的类可以直接实例化，但不具备任何抽象基类的功能
# 3.不能直接实例化，只能被继承
# 4.子类可以不重写或重写部分抽象方法，已经实现的方法也可以不重写，但是只有实现了所有抽象方法的子类才可以实例化
# 5.定义的抽象方法也可以实现，但一般只做简单的基础实现
# 6.子类可以通过super()去调用抽象方法或已经实现的方法，目的是为了保证多重继承中super()链的完整性
# 7.抽象类可以单继承或多继承，但不推荐多继承

# 抽象基类的使用场景


from abc import ABCMeta, ABC, abstractmethod


# 模拟抽象基类的实现
class A(object):
    def get(self):
        raise NotImplementedError

    def set(self):
        raise NotImplementedError


class B(A):
    # 子类必须要实现所有抽象方法
    pass


b = B()


# b.get()
# 通过在基类方法中抛出NotImplementError的方式模拟抽象基类
# 可以看到虽然没有实现A类的所有抽象方法，但仍然可以实例化B类，只有在调用了对应方法之后才会抛出异常


# 使用abc模块实现抽象基类
class A(ABC):  # 以继承的方式定义抽象基类
    # metaclass=ABCMeta 以元类的方式定义抽象基类
    # ABC类是一个使用ABCMeta作为元类的工具类，抽象基类可以通过从ABC派生来简单地创建。
    # @abstractmethod可以装饰实例方法、类方法、静态方法、属性，@abstractmethod必须放在装饰器的最下层
    # ABC的实现是这样的：
    # class ABC(metaclass=abc.ABCMeta):
    #     __slots__ = ()
    # 而ABCMeta的实现是这样的。
    # 首先每个@abstractmethod会给装饰的函数增加一个__isabstractmethod__的属性。
    # 此后，对于某个继承自抽象基类的类，ABCMeta会在__new__中检查该类及所有基类中所有__isabstractmethod__ = True的方法，
    # 组成一个集合。下一步，检查该类中所有没有__isabstractmethod__属性或属性为False的方法，并与上一步的集合做差。
    # 如果结果的集合不为空，则该类仍旧是抽象基类，不可实例化。
    @abstractmethod
    def object_get(self): pass

    @classmethod
    @abstractmethod
    def class_get(cls): pass

    @staticmethod
    @abstractmethod
    def static_get(): pass

    @property
    @abstractmethod
    def property_get(self): pass


class B(A):
    def object_get(self):
        print("实例方法")

    @classmethod
    def class_get(cls):
        print("类方法")

    @staticmethod
    def static_get():
        print("静态方法")

    @property
    def property_get(self):
        return "属性装饰器"


# A()
# TypeError: Can't instantiate abstract class A with abstract methods class_get, object_get, property_get, static_get
# 如果尝试实例化一个抽象基类，那么直接就抛出异常了
B().object_get()
B().class_get()
B().static_get()
print(B().property_get)


# 没有定义任何抽象方法，可以实例化，但是没有抽象基类的功能
class A(ABC):
    pass


A()


class A(ABC):
    def a(self):
        print("A.a 抽象基类中就已经实现的方法")

    @abstractmethod
    def b(self):
        print("A.b 抽象方法中也可以做部分实现")

    @abstractmethod
    def c(self): pass


class B(A):
    def b(self):
        # 通过super()去调用抽象方法或已经实现的方法
        super().a()
        super().b()
        super().c()

    def c(self):
        print("B.c 抽象方法在子类的实现")


B().a()
B().b()
B().c()


# 抽象基类遵循接口的规范也可以当成接口使用，实现接口的多继承
class WalkAnimal(ABC):
    @abstractmethod
    def walk(self):
        print('walk')


class SwimAnimal(ABC):
    @abstractmethod
    def swim(self): pass


class FlyAnimal(ABC):
    @abstractmethod
    def fly(self): pass


# 如果正常一个老虎有跑和跑的方法的话，我们会这么做
# class Tiger:
#     def walk(self):pass
#     def swim(self):pass
# 但是我们使用接口类多继承的话就简单多了，并且规范了相同功能
class TigerBase(WalkAnimal, SwimAnimal):
    pass


# 如果此时再有一个天鹅swan,会飞，会走，会游泳 那么我们这么做
class SwanBase(WalkAnimal, SwimAnimal, FlyAnimal):
    pass


# 再去实现
class Tiger(TigerBase):
    def walk(self):
        print("老虎walk")

    def swim(self):
        print("老虎swim")


class Swan(SwanBase):
    def walk(self):
        print("天鹅walk")

    def swim(self):
        print("天鹅swim")

    def fly(self):
        print("天鹅fly")


tiger = Tiger()
tiger.walk()
tiger.swim()
swan = Swan()
swan.walk()
swan.swim()
swan.fly()


# 抽象基类的使用场景
# 1.检查对象是哪种类型（就是检查这个对象有没有实现该类型应该实现的接口）
# 因为鸭子类型的存在，Python中判断一个对象是什么类型是通过看它定义了什么方法、属性，不像Java中需要指定它的类型
# 鸭子类型多与魔术方法结合使用，内置的数据类型都有对应的魔术方法，实现了对应魔术方法的对象都可以称为是某种数据类型
# 实现了__len__()，那它就是Sized类型；实现了__iter__()、__next__()，那它就是Iterable类型等等。
# 当然也可以规定实现a()的类为某某类型，则其他实现了a()的类都可以称为某某类型
# Python内置了一些常见类型的抽象基类，例如：
# <常见的数据结构>在collection.abc模块
# <数字类型>在numbers模块
# <流>在io模块
# <导入查找器和加载器>在importlib.abc模块

# 第一种方式：使用hasattr()
class Company(object):
    def __init__(self, employee):
        self.employee = employee

    def __len__(self):
        return len(self.employee)


com = Company(["a", "b", "c"])
# 类方法也称为类属性
print(hasattr(com, "__len__"), "使用hasattr()检查类中是否有__len__属性")

# 第二种方式：使用isinstance()
# 如果给定的类对象是一个抽象基类，则isinstance()会调用抽象基类的__subclasshock__()
from collections.abc import Sized
print(isinstance(com, Sized))


# 2.强制子类必须实现某些方法
class A(object):
    @abstractmethod
    def a(self): pass
    @abstractmethod
    def b(self): pass


class B(A):
    def a(self): print("B中需要实现A的a()")
    def b(self): print("B中需要实现A的b()")


b = B()
b.a()
b.b()


# 参考链接
# https://zhuanlan.zhihu.com/p/51216183
# https://zhuanlan.zhihu.com/p/89549054
# https://mp.weixin.qq.com/s/dz77b2Q7ynaGKLiqntIrHg
