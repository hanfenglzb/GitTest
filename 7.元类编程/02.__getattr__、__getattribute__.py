# __getattr__(): 在通过点运算符查找不到属性时，如果定义了__getattr__()，则调用__getattr__()做最后的尝试
# __getattribute__(): 通过点运算符或getattr()访问属性时进入该方法，若访问的属性不存在，则抛出AttributeError

def object_getattribute(obj, name):
    """Emulate PyObject_GenericGetAttr() in Objects/object.c"""
    null = object()
    objtype = type(obj)
    cls_var = getattr(objtype, name, null)
    descr_get = getattr(type(cls_var), '__get__', null)
    if descr_get is not null:
        if (hasattr(type(cls_var), '__set__')
                or hasattr(type(cls_var), '__delete__')):
            return descr_get(cls_var, obj, objtype)  # data descriptor
    if hasattr(obj, '__dict__') and name in vars(obj):
        return vars(obj)[name]  # instance variable
    if descr_get is not null:
        return descr_get(cls_var, obj, objtype)  # non-data descriptor
    if cls_var is not null:
        return cls_var  # class variable
    raise AttributeError(name)


# 属性查找钩子函数：
def getattr_hook(obj, name):
    """Emulate slot_tp_getattr_hook() in Objects/typeobject.c"""
    try:
        return obj.__getattribute__(name)
    except AttributeError:
        if not hasattr(type(obj), '__getattr__'):
            raise
    return type(obj).__getattr__(obj, name)  # __getattr__


# 通过点运算符、getattr()访问属性时将自动调用上面的getattr_hook()函数，在getattr_hook()里面调用__getattribute__()
# 如果__getattribute__()中没有查找到对应属性，则抛出AttributeError，
# 如果定义了__getattr__()，则调用__getattr__()做最后的尝试。
# 如果程序中主动调用__getattribute__()，则getattr_hook()的自动调用将会被绕过，同样也不再调用__getattr__()
# 但是重写这些方法，getattr_hook()还是自动调用，因为默认也是object.__getattribute__，如果重写了，则调用自定义的
# 在object类、type类中都有__getattribute__()，分别定义了通过实例访问（object）和通过类访问属性的查找方式。

# __getattribute__()一般不需要重写，object和type类中的__getattribute__()使用C语言编写，对属性的查找已经足够正确且高速
# 如果重写，那么一定需要保证对属性查找的准确性，正确抛出AttributeError，且不能在__getattribute__()中编写任何通过.运算符、getattr()，
# 甚至是self.__dict__["attr"]的方式，对实例字典的访问不会触发__getattribute__()，但是self.__dict__是点运算符访问！
# 否则又会触发调用__getattribute__()，导致无限递归！

# 并不是所有属性通过点运算符或getattr()访问时都会触发对__getattribute__()的调用
# Python的一些内置函数其实就是调用类中的特殊方法，例如：len(obj) 等价于 obj.__len__()，但是两种调用的访问过程并不一致
# 前者会隐式调用特殊方法，这种隐式调用会绕过__getattribute__()，由解释器控制访问
# 后者是显式调用特殊方法，显示调用就跟类中普通方法的访问一样，自动调用get_hook()
# 特殊方法跟普通方法是一样的非数据描述符，也属于实例方法、类方法、静态方法中的一种


class A(object):
    def __init__(self, a):
        self.a = a
        self.b = 1
        self.infos = {"c": 3}
        self.b = B()

    def add(self):
        return self.a + self.b

    # def __getattr__(self, item):
    #     return self.infos.get(item, repr(item) + " is not exist")
    def __getattr__(self, item):
        # return self.b.p  # 通过.运算符就必须固定写p，没办法用变量
        return getattr(self.b, item)


class B(object):
    def p(self, value):
        return value


aa = A(2)
# print(aa.c, aa.d)
res = aa.p(1)
# 分为两步：
# 1.aa.p -> 访问p属性，发现实例和类中都没有，则调用__getattr__()，将属性p的名称"p"作为item参数传入，
# 根据"p"，通过getattr()，在B类的实例self.b中获取名为"p"的属性并返回
# 2.得到的属性是名为p的方法对象，然后通过xxx()的方式调用p方法对象
print(res)


# 通过.运算符获取/设置/删除字典项
class DotDict(dict):
    def __getattr__(self, item):
        return self.__getitem__(item)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __delattr__(self, item):
        self.__delitem__(item)


print(" dot_dict ".center(20, "-"))
dot_dict = DotDict()
dot_dict["a"] = 1
print(dot_dict.a)
# print(dot_dict.b) # KerError
dot_dict.b = 2
print(dot_dict.b)
del dot_dict.a
print(dot_dict)


