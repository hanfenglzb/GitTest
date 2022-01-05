# 实例方法
# from types import MethodType
class MethodType:
    # 模拟内置的MethodType类
    ...

    def __init__(self, func, obj):
        self.__func__ = func
        self.__self__ = obj

    # 函数对象是内置的非数据描述符（只定义了__get__()函数），通过.运算符访问类中的函数时
    # 触发描述符特性，调用函数对象的__get__()方法，返回一个MethodType实例（该实例需要两个参数：函数对象和实例对象）
    # 而后调用这个MethodType实例，触发__call__()方法，调用这个函数，将实例对象作为函数的第一个参数传入，返回函数值
    def __call__(self, *args, **kwargs):
        func = self.__func__
        obj = self.__self__
        return func(obj, *args, **kwargs)


class Function:
    ...

    def __get__(self, instance, owner):
        # instance为空，表示并不是通过实例调用
        # 也就是通过类调用，则返回函数对象本身
        if instance is None:
            return self
        # 通过实例调用的情况下，将函数对象和实例传入MethodType类，返回MethodType类型
        return MethodType(self, instance)


# 函数对象中定义了__get__()，当它在类中定义时，属于一个类属性，这个时候就会被当成一个非数据描述符
# 当通过.运算符访问函数对象时，触发函数对象中定义的__get__()函数
# 如果是通过类调用，则返回函数对象本身；
# 如果是通过类实例调用，则返回MethodType(func, obj)实例
# 而MethodType类中定义了__call__()函数，所以MethodType(func, obj)实例是一个可调用对象
# 可以以MethodType(func, obj)(*args, **kwargs)方式调用，并且在__call__()函数中会将obj作为第一个参数传递给函数对象
# 实现了以实例调用类中定义的函数的时候，自动将实例作为第一个参数传递给函数（即实例方法）
# obj.func(self, *args, **kwargs) -> func(obj, *args, **kwargs)
# 调用过程：
# 通过实例调用
# 1. obj.func -> type(obj).__dict__["func"].__get__(obj, type(obj)) -> return MethodType(func, obj)
# 2. obj.func(*args, **kwargs) -> MethodType(func, obj)(*args, **kwargs)
# -> MethodType(func, obj).__call__(*args, **kwargs) ->  return func(obj, *args, **kwargs)
# 通过类调用：
# 1. cls.func -> cls.__dict__["func"].__get__(None, cls) -> return func
# 2. cls.func(*args, **kwargs) -> func(cls(), *args, **kwargs)
# 示例如下：
class Test:
    def __init__(self, value):
        self.value = value

    def test(self, access_type):
        print(self.value, access_type)


t = Test(1)
print(t.test)  # 实例访问
print(Test.test)  # 类访问
print(Test.__dict__["test"])  # 类的__dict__访问
print(getattr(t, "test"), getattr(Test, "test"))  # getattr()函数访问，等价于通过.运算符访问
t.test("obj")  # 类实例访问并调用
Test.test(t, "class")  # 类对象访问并调用
Test.__dict__["test"](t, "class.__dict__[attr]")  # 类对象的__dict__属性访问并调用
getattr(t, "test")("getattr(obj, attr)")  # getattr()函数访问并调用-类实例
getattr(Test, "test")(t, "getattr(class, attr)")  # getattr()函数访问并调用-类对象


# 模拟实现实例方法
# 以装饰器形式传递函数对象到自定义的描述符中，绕过.运算符方式，避免直接触发函数描述符，模拟函数到实例方法的转变
# from typing import MethodType
# from functools import partial
class InstanceMethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            # 函数类中的__get__()的话，此处应该返回函数对象自身，也就是self
            return self.func
        return MethodType(self.func, instance)  # Method
        # return partial(self.func, instance)   # partial
        # func.__defaults__ = (instance,)       # func.__defaults__
        # return func


class A:
    def __init__(self, value):
        self.value = value

    @InstanceMethod
    def test(self):
        print(self.value)


a = A(2)
a.test()

# 实例方法的作用就是会自动将实例作为函数的第一个参数传入，Python的默认方式是返回一个typing.MethodType类实例
# 这将使其变成一个绑定方法。可以模拟这个MethodType类，在函数的__get__()函数中返回自定义的MethodType类实例
# 模拟将一个类中定义的函数变成一个实例方法的代码如上；当然，最终的目的就是让实例作为第一个参数传入而已，所以也可以使用partial()
# 返回新的函数对象，或者直接设置函数对象的__defaults__，将实例传入，返回原来的函数对象。
# 总之，只要能将实例传入原函数，并返回一个可调用对象即可。


print("动态添加方法".center(30, "-"))


class B:
    def __init__(self, value):
        self.value = value

    # 实例方法
    def set_value(self, value):
        self.value = value


# 动态添加实例方法
b = B(0)
b.set_value("b")
# 第一步: b.set_value -> type(b).__dict__["set_value"].__get__(b, type(b)) -> return MethodType(set_value, b)
# 第二步: b.set_value(value) -> MethodType(set_value, b).__call__(value) -> return set_value(b, value)
# 这样的话可以在外部动态添加实例方法，访问类内的函数就是调用函数的__get__()，最终返回一个MethodType()实例
# 可以直接将实例属性设置成MethodType()类实例
from types import MethodType

# 1. 实例设置一个函数
# 实例属性如果直接设置为一个函数，那么这个函数不构成一个描述符，就是一个普通的函数对象，这相当于给实例设置了一个静态方法
b.get_value0 = lambda x: x + 1
print(b.get_value0(1))

# 2. 实例设置一个MethodType实例
b.get_value = MethodType(lambda self: self.value, b)
res = b.get_value()
# b.get_value() => MethodType(get_value, b).__call__()
# 实例通过点运算符方法访问动态添加的MethodType实例和访问定义在类中的函数是有区别的
# 后者会触发函数的描述符，然后再返回一个MethodType实例；前者就是直接访问添加的MethodType实例。
print(res, "obj_b")
print(vars(b))

# 3. 类对象设置一个函数
# 该函数成为类属性，也就是描述符，和正常在类中定义的一样
B.get_value = lambda self: self.value
b1 = B("b1")
res1 = b1.get_value()
print(b1.get_value)
print(res1, "obj_b1")
print(vars(b1))

# 4. 类对象设置一个MethodType实例
B.get_value1 = MethodType(lambda self: self.value, B)
print(B.get_value1)
# 传递给MethodType类的obj参数为A类对象，则self参数为A，访问A的类属性value
# 那么就成为了一个类方法
B.value = "B"
res2 = B.get_value1()
print(res2, "class_B")


# 静态方法
class StaticMethod:
    def __init__(self, func):
        self.func = func

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        return self.func


# 类方法
class ClassMethod:
    def __init__(self, func):
        self.func = func

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        if owner is None:
            owner = type(instance)
        # 使其支持链式调用
        if hasattr(type(self.func), "__get__"):
            # 获取self.func的类型，如果该类中有__get__属性（如果是一个描述符）
            # 则调用self.func的__get__()，并传入owner，作为def __get__(instance, owner):中instance参数的值
            return self.func.__get__(owner)
        return MethodType(self.func, owner)


class Datetime:
    def __init__(self, year, mouth, day):
        self.year = year
        self.mouth = mouth
        self.day = day

    @StaticMethod
    # from_str_static = StaticMethod(from_str_static)
    def from_str_static(string):
        # 在类中不需要用到实例对象，类对象的方法，可以定义成静态方法，静态方法是定义在类中的工具函数
        print("static method")
        # 静态方法中一样可以返回类实例，但是这样类名就被硬编码了
        return Datetime(*map(int, string.split("-")))

    @ClassMethod
    def from_str_class(cls, string):
        # 需要用到类对象的方法（例如需要返回类实例、用到类属性等），可以定义成类方法
        print("class method")
        # 定义成类方法，第一个参数cls会自动传递类对象
        return cls(*map(int, string.split("-")))


d = Datetime(2021, 11, 9)
d_s = d.from_str_static("1998-12-15")
print(d_s)
d_c = Datetime.from_str_class("1998-12-15")
print(d_c)

# 静态方法不需要自动传递实例对象或类对象。
# 在函数的__get__()中，通过类调用会返回原函数对象，通过实例调用会返回一个MethodType实例
# 要实现静态方法，就需要将函数的__get__()的返回值改写，使其通过实例或类调用都返回原函数对象
# 所以可以自定义一个描述符类，将函数作为参数传入，在自定义描述符的__get__()方法中返回原函数对象
# 调用顺序:
# 通过实例调用：
# 1. obj.func -> type(obj).__dict__["func"].__get__(obj, type(obj)) -> return func
# 2. obj.func(*args, **kwargs) -> func(*args, **kwargs)
# 通过类调用：
# 1. cls.func -> cls.__dict__["func"].__get__(None, cls) -> return func
# 2. cls.func(*args, **kwargs) -> func(*args, **kwargs)

# 类方法需要自动传递类对象
# 实现类方法类似实现实例方法，只是通过实例或者通过类调用都可以自动传递类对象
# 默认的实现方式是返回一个MethodType实例，将其中的obj传入类对象即可
# 调用顺序:
# 通过实例调用：
# 1. obj.func -> type(obj).__dict__["func"].__get__(obj, type(obj)) -> return MethodType(func, type(obj))
# 2. obj.func(*args, **kwargs) -> MethodType(func, type(obj)).__call__(*args, **kwargs)
# -> return func(type(obj), *args, **kwargs)
# 通过类调用
# 1. cls.func -> cls.__dict__["func"].__get__(None, cls) -> return MethodType(func, cls)
# 2. cls.func(*args, **kwargs) -> MethodType(func, cls).__call__(*args, **kwargs)
# -> return func(cls, *args, **kwargs)


# class ClassMethod:
#     def __init__(self, func):
#         self.func = func
#
#     def __set_name__(self, owner, name):
#         self._name = name
#
#     def __get__(self, instance, owner):
#         if owner is None:
#             owner = type(instance)
#         # 使其支持链式装饰器调用
#         if hasattr(type(self.func), "__get__"):
#             return self.func.__get__(owner)
#         return MethodType(self.func, owner)


# classmethod支持链式调用
class D:
    @classmethod
    @property
    # __doc__ = property(__doc__)
    # __doc__ 重新赋值为一个property描述符
    # __doc__ = classmethod(__doc__)
    # __doc__ 重新赋值成为classmethod描述符
    def __doc__(cls):
        return f"{cls.__class__}"


d = D()
print(d.__doc__)
# 在通过点运算符访问__doc__时，触发调用__doc__的__get__()，又因为__doc__先前是一个property描述符对象
# 也就是__doc__实例的self.func是一个property描述符对象，所以hasattr(type(self.func), "__get__")为True
# 将返回self.func.__get__(owner)，即通过property描述符对象调用property描述符类的__get__()，
# 并将owner作为__get__(instance, owner)的instance参数传入，然后return self.func(owner)，这个func才是原始的函数对象
# 调用过程：
# @property的过程：__doc__ = property(__doc__) -> 函数对象被转变成property描述符
# @classmethod的过程：__doc__ = classmethod(__doc__) -> property描述符被转变成classmethod描述符
# obj.__doc__的过程：obj.__doc__ (此时__doc__为classmethod描述符)
# -> type(obj).__dict__["__doc__"].__get__(obj, type(obj))
# -> return __doc__.__get__(type(obj)) (此时__doc__为property描述符)
# -> return __doc__(type(obj)) (此时__doc__为函数对象)

