# 什么是属性描述符：实现了__get__/__set__/__delete__任意一个或多个的类
# 在不涉及属性描述符的时候，通过a.x去查找一个属性时，其优先级为：
# a.__dict__["x"]->type(a).__dict__["x"]-> type(a)的mro解析顺序的类的__dict__["x"]
# 定义在父类的实例属性的优先级？父类并没有实例化，在进行初始化实例属性的时候实际上传入的是子类的实例
# 那也就是根据父类实例属性的语法定义了一个子类实例的属性，加入到子类的实例字典中，就算不是显式传入子类实例也是一样的，
# 比如子类继承了父类，但是子类直接pass，什么也没做，这时并没有显式的传入子类实例给父类初始化方法或其他方法去初始化这个属性，
# 但父类的实例属性仍然会被加入到子类的实例字典中。
# 父类类属性的优先级？父类类属性保存在父类对象中，子类类属性保存在子类类对象中，按正常的子类 -> 父类的顺序访问
# 通过实例可以访问实例的变量、类中的变量和方法等所有的属性，但通过类不能访问在实例中的变量
# 实例访问实例方法时，会自动传入实例本身；类访问实例方法时，不会自动传入，需要手动传入

# 数据描述符：实现了__set__()或者__delete__()其中一个或两个
# 非数据描述符：只实现了__get__()
# 在有描述符存在时，查找顺序为：
# 实例调用：数据描述符（包括父类中的数据描述符） -> 实例__dict__（父类的实例属性也在子类的实例字典中） -> 非数据描述符 -> 类字典 -> __mro__[i]字典（父类） -> __getattr()__
# 类调用：数据描述符 -> 类字典 -> 非数据描述符 -> __mro__[i]字典（父类） -> __getattr__()
# super()调用：在__mro__中按上述类调用的方式查找


class A(object):
    def __init__(self):
        self.a = 0

    def __get__(self, instance, owner=None):
        print("__get__()")
        return self.a

    def __set__(self, instance, value):
        print("__set__()")
        self.a = value

    def __delete__(self, instance):
        print("__delete__()")
        del self.a


class B(object):
    a = A()


b = B()
b.__dict__["a"] = "a"
print(b.a, B.a)
# B.a = 1
b.a = 1
print(B.__dict__, b.__dict__)


# 1.实现了__get__/__set__/__delete__中的任意一个或多个方法的类
# 2.其实例定义为一个类（一般称为托管类或所有者类）的类属性
# 3.可以通过托管类或其实例调用，通过类调用，则__get__(self, instance, owner)的instance为None
# 通过实例调用，则instance为该实例

# 至于__get__/__set__/__delete__方法中需要怎么去定义，则要看具体想实现什么了
# 如下实现对学生不同科目分数的托管（或者叫代理），因为分数设置为多少是有限制的
# 这样就必须写一定的判断逻辑，这种判断如果比较少，可以写在初始化方法中
# 但如果多个属性都需要相同的判断，那么可以使用描述符进行托管
# 比如property就是描述符，但是property是用作类中方法的代理，只适合属性较少的情况
# 如果想要高度定制，可以自定义描述符

class Score:
    def __init__(self, attr):
        self.attr = attr

    # 现在的版本中可以使用__set_name__()，不用再硬编码传递attr
    def __set_name__(self, owner, name):
        self.name = name
        self._name = f"_{name}"

    def __get__(self, instance, owner):
        return self.attr, instance.__dict__[self.attr]

    def __set__(self, instance, value):
        if not isinstance(value, (int, float)):
            raise TypeError("score must be integer or floating-point")
        if not 0 <= value <= 100:
            raise ValueError("score must be in [0,100]")
        instance.__dict__[self.attr] = value

    def __delete__(self, instance):
        instance.__dict__[self.attr] = 0


class Student:
    math = Score("math")
    chinese = Score("chinese")
    english = Score("english")

    def __init__(self, math, chinese, english):
        self.math = math
        self.chinese = chinese
        self.english = english


stu = Student(100, 79, 69)
print(stu.math)
print(stu.__dict__)


# 使用property描述符
class B:
    def __init__(self):
        self._val = 1

    def get_val(self):
        return self._val

    def set_val(self, value):
        # if...
        self._val = value

    def del_val(self):
        self._val = 0

    val = property(
        fget=get_val,
        fset=set_val,
        fdel=del_val
    )


b = B()
print(b.val)
b.val = 100
print(b.val)


# 简单模拟一个property描述符
class Property:
    def __init__(self, fget=None, fset=None, fdel=None):
        # 初始化描述符的时候将需要代理的方法传递进来
        self.fget = fget
        self.fset = fset
        self.fdel = fdel

    def __get__(self, instance, owner):
        # 调用实例方法并返回执行结果
        # fget在描述符初始化的时候被传入，所以直接调用即可
        # 需要注意传进来的是函数对象，不能看成绑定在类对象上的方法，所以需要手动传入实例
        print(self.fget)
        return self.fget(instance)
        # 但是，这只是其中一种方式，如果不传入函数对象，而是传入函数名称，或者直接不传入是否可以呢？
        # 一般不会不传入，因为这个描述符要针对不同的函数，除非只针对固定的函数，这个时候在代码里写死也行
        # 只传入函数名称则可以通过类对象调用(类中定义的方法不会存在实例的__dict__中)
        # return owner.__dict__[self.fget](instance)

    def __set__(self, instance, value):
        self.fset(instance)

    def __delete__(self, instance):
        self.fdel(instance)

    # 实现装饰器语法
    def getter(self, instance):
        # @attr.getter
        # attr = getter(attr)
        return self.fget(instance)



class C:
    def __init__(self):
        self._c = 1

    def get_c(self):
        return self._c

    c = Property(
        fget=get_c,
    )


cc = C()
print(cc.c)

# 其他的描述符见目录<描述符>
