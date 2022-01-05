# property属性访问
class Property:
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        # 这里为什么需要传递函数对象进来，在后面直接通过类或实例去调用不就可以了？
        # 通过类调用，需要手动传递一个实例对象作为函数的self参数
        # 而且不管是通过.运算符还是getattr()还是__dict__[]的方式
        # 要么写死代码，要么要给出函数的名称
        # 最好的做法就是直接在实例化描述符的时候传递函数对象进来
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and self.fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __set_name__(self, owner, name):
        print(id(self), "__set_name__")
        # 编译的时候调用该函数，将描述符的名称保存，后面需要使用的话可以调用这里的，就不需要在初始化的时候手动传递
        self._name = name

    def __get__(self, instance, owner):
        # 这里是实现通过.运算符调用，只需要直接调用这个函数，返回一个值，不需要其他操作
        # 如何调用：将函数对象传递进来，这里传递的是没有绑定的原生函数对象
        if instance is None:
            # 如果是通过类调用的话，返回描述符实例对象本身
            return self
        if self.fget is None:
            # 如果在初始化描述符的时候没有传递函数对象进来，那么表示该描述符没有应用于读取属性的方法中，应该抛出AttributeError
            raise AttributeError(f"unreadable attribute {self._name}")
        # 这里传递的函数是原生函数对象，所以需要传递实例作为其self参数
        return self.fget(instance)

    def __set__(self, instance, value):
        # 为什么不用判断instance为None的情况？
        # 通过类对描述符做设置操作，会将描述符覆盖，成为一个类属性，不会触发__set__()
        if self.fset is None:
            raise AttributeError(f"can't set attribute {self._name}")
        self.fset(instance, value)

    def __delete__(self, instance):
        # 同fset，通过类对描述符做删除操作，直接删除了描述符，不会触发__delete__()
        if self.fdel is None:
            raise AttributeError(f"can't delete attribute {self._name}")
        self.fdel(instance)

    # 装饰器实现
    # 装饰器语法只是改变了传递fget、fset、fdel参数的方式
    # getter()不需要实现，通过@Property语法，会传递紧跟着的函数对象
    # 而fget是Property类的第一个参数，也就是设置了fget，这和getter()做的事是一样的
    # def getter(self, fget):
    #     prop = type(self)(fget, self.fset, self.fdel)
    #     # prop._name = self._name
    #     return prop

    def setter(self, fset):
        # 创建新的描述符对象
        prop = type(self)(self.fget, fset, self.fdel)
        print(id(self), "set self")
        print(id(prop), "set prop")
        # 通过装饰器语法生成的描述符对象因为没有赋值给一个标识符，并不会调用__set_name__()
        # _name属性还不存在
        # prop._name = self._name
        return prop
        # 不创建新的描述符对象
        # 可以原返回第一个Property对象，原本self.fset为默认值None
        # 将其赋值为传递进来的fset函数对象即可，不生成新的Property对象，self.fdel同理
        # self.fset = fset
        # return self

    def deleter(self, fdel):
        # 创建新的描述符对象
        prop = type(self)(self.fget, self.fset, fdel)
        print(id(self), "del self")
        print(id(prop), "del prop")
        # prop._name = self._name
        return prop
        # 不创建新的描述符对象
        # self.fdel = fdel
        # return self

    def set_doc(self, doc=None):
        if doc is None and self.fget.__doc__ is not None:
            doc = self.fget.__doc__
        self.__doc__ = doc
        return self


class A:
    def __init__(self, name, age, gender):
        self._name = name
        self._age = age
        self._gender = gender

    # property描述符类
    @property   # name = property.getter(name)
    def name(self):
        return self._name

    @name.setter    # name = property.setter(name)
    def name(self, value):
        self._name = value

    @name.deleter
    def name(self):
        self._name = None

    # 自定义的Property描述符类
    @Property
    # age = Property(age)
    # 这时的age被转换成了Property的一个实例（描述符），该实例只传递了一个参数fget，fset、fdel为默认的None
    # 如果定义了getter()，则可以使用@Property().getter的方式
    # 等价于 age = Property().getter(age)
    def age(self):
        return self._age
    print(id(age), "get out")

    @age.setter
    # age = age.setter(age)
    # @age.setter装饰器只能在@Property后面使用，否则age只是一个函数对象，没有变成描述符
    # 或者通过@Property().setter方式使用使其变成只写，否则setter()中的self不会自动传递
    # @age.setter中的age已经是Property的一个实例，通过age实例调用Property类中setter()
    # 生成一个新的描述符对象，fset参数设置为下方的age函数，fget和fdel设置为之前的age描述符中的fget函数对象和None
    # 返回这个新的描述符对象，此时这个新的描述符设置了fget和fset参数，fdel参数则为None
    # 而上一步中的@Property生成的描述符实例最后会因为没有引用而被回收
    def age(self, value):
        self._age = value
    print(id(age), "set out")

    @age.deleter
    # age = age.getter(age)
    # deleter装饰器也只能在@Property后面使用
    # 因为这里也定义了setter，所以此时的age.deleter中的age是上面setter中返回的描述符实例
    # 通过该实例调用Property类中的deleter()
    # 同样生成一个新的描述符对象，fdel参数设置为下方的age函数，fget和fset设置为之前的age描述符中的fget和fset函数对象
    # 返回这个新的描述符对象，此时这个新的描述符设置了fget、fset、fdel参数
    # 上一步@age.setter中生成的描述符实例最后会因为没有引用而被回收
    def age(self):
        self._age = None
    print(id(age), "del out")
    # 函数也属于类属性，以上过程会发生在类的创建过程中
    # 在最后，类中会生成一个名称为age的Property描述符
    # 类中age属性的性质被固定，即：age = @age.deleter返回的Property描述符对象
    # 这一步将触发__set_name__()方法，设置_name属性
    # 装饰器方式的默认写法会导致@Property、@attribute.setter、@attribute.deleter三个地方都生成一个Property对象
    # 当然也可以改写使其除了@Property处生成新的对象，后面两处在设置完fset或fdel后原返回之前的对象
    # 通过装饰器语法生成Property描述符和age = Property(...)语法生成本质上是一样的

    # 设置gender描述符为只写属性（只设置fset参数）
    @Property().setter
    def gender(self, value):
        self._gender = value


a = A("ann", 23, "男")
print(a.age, a.name)
a.age = 18
a.name = "ppq"
print(a.age, a.name)
print(a.__dict__)
print(A.__dict__)
a.gender = "女"

# 函数是一个非数据描述符，@property、@staticmethod、@classmethod等为什么先起作用了？
# 用作装饰器语法时，将函数对象作为参数传递到类中，生成对应的实例对象并返回（数据描述符）
# 原先的函数对象被替换成了对应的描述符对象，通过点运算符调用的时候，是访问的描述符对象而不是原先的函数对象
# 装饰器语法可以使原函数名替换成一个描述符，隐藏原先的函数（推荐使用）

# 用作正常的实例化方式时，如下:
# name = property(fget=..., fset=..., fdel=...)
# static_func = staticmethod(func)
# class_method = classmethod(func)
# 原函数名不会被替换成描述符对象，而是新定义了一个描述符名，可以各自独立访问

