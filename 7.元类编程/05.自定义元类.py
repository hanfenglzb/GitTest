# 类也是对象，是Python中一等公民
# 可以和操作普通对象一样操作类对象，不同的是，这些操作将会反映到该类对象的所有实例上
# 例如有一个A类，则A.a = 1 -> a是A类的类属性

def class_factory():
    class User:
        pass

    return User


User = class_factory()
user = User()
User.name = "aaa"
print(user, user.name)

# 类是一种对象，那么类也有类型，类的类型就称为元类，也就是元类用于创建类对象
# Python中所有类对象的默认元类是type类，也就是所有的类对象都是type类的实例，包括type类自身
# 那么我们就可以用type类去创建类，就跟用类去创建类实例一样

# type(what: object, bases=None: tuple, dict=None: dict)
# 1. type(object) -> object的类型对象
print(type("a"))


# 2. type(name, bases, dict, **kwds) -> 新类型
# name：类名
# bases：类的基类。class关键字定义类时，在类名后面的括号中定义的基类列表
# dict：类属性
# **kwds：见__init_subclass__()的用法
class A:
    pass


def __init__(self, name):
    self.name = name


User = type("User", (A,), dict(name="cls_name", __init__=__init__))
# 元类实例化的方式定义一个类等价于使用class关键字创建类的过程
# class User(A):
#     name = "cls_name"
#
#     def __init__(self, name):
#         self.name = name

user = User("obj_name")
print(user.name, User.name)
print(User.__name__, User.__mro__, User.mro(), user.__class__, User.__class__, User.__bases__)


# 自定义元类
# 元类是类的类型，用于创建类，默认情况下，所有类的元类都是type类
# 如果需要通过元类来控制类的创建过程，那么只能继承type类，在type类的子类中去重写type类的方法
# 而这个type类的子类其实也是type类的实例
# 如下，创建一个自定义的元类，只是这个元类没有做任何事：
class Meta(type):
    pass


# 上面的过程等价于：Meta = type("Meta", (type,), {})
# 这个自定义的Meta元类继承自type类，具有type类的所有属性，同样可以用来动态创建类
# 通过自定义元类创建类：
# 1. 元类实例化的方式
B = Meta("B", (), {})
b = B()


# 2.class关键字的方式，显示指定metaclass参数为某个元类
# 也可以继承一个包含metaclass参数的类，abc模块的ABC类就是继承了ABCMeta元类：class ABC(metaclass=ABCMeta): ...
class C(metaclass=Meta):
    pass


# __new__和__init__
# 1.在普通类中重写__new__和__init__
class D:
    # __new__()：
    # 是一个静态方法（特例，不需要显示的@staticmethod声明），重写它至少需要定义一个cls参数。
    # 在该类实例化一个对象时，会被解释器自动调用，同时会将类自身作为cls参数传入，如果显示调用，则需要主动传入一个类对象。
    # 如果还有其他参数那么会传递给对象构造器表达式，用于在后面传递给__init__()(如果定义了的话，没有定义则不调用；__init__()的形参列表需要定义成能够全部且正确的接收这些参数才行)
    # 需要返回一个实例对象（通常就是cls类的实例），那么后续就会再自动调用这个实例对象的__init__()方法
    # 如果没有返回值或者返回一个其他类的实例对象，则不会再调用__init__()，并且
    # __new__()方法是类的构造方法，在__new__()中构造生成一个实例对象
    # __init__()方法是实例的初始化方法，在__init__()中对实例对象进行一些初始化操作

    # 构造类的实例是解释器做的事，我们可以自定义__new__()

    # __new__方法的调用时间（以D类为例）：当调用D类生成一个实例对象时 => D(*args, **kwargs)，
    # 根据D类的__mro__属性，按顺序逐个尝试调用D类自身或其基类的__new__()方法
    # 直到顶层基类object的__new__()；如果成功调用某个类的__new__()，就将D类对象（这个时候类对象已经生成）作为cls参数传入
    def __new__(cls, *args, **kwargs):
        print(cls, args, kwargs)
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        print(self, args, kwargs)


print(D.__mro__)
d = D(1, 2, c=3)


# 2.在元类中重写__new__和__init__
class Meta(type):
    def __new__(mcs, *args, **kwargs):
        print("元类的__new__")
        return super().__new__(mcs, *args, **kwargs)

    def __init__(cls, *args, **kwargs):
        print("元类的__init__")
        super().__init__(*args, **kwargs)



