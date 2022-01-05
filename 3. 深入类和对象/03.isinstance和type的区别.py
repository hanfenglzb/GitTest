# isinstance()
# 检查一个对象的类型是否是指定的类(类型有多个以元组形式传递，是否是这些类型中的一个)
print(isinstance([], list))  # True
print(isinstance([], (set, list)))  # True
print(isinstance(list, type))  # True
print(isinstance(list, object))  # True
# list是type类的实例，type类也继承自object类，所以list类对象也是object类的实例
# type()
# 返回的是这个对象的类对象
print(type([]))
print(type(list))
print(type(1) is int)  # True -> type()返回int类对象，再使用is判断是否为同一个int类对象


# 判断一个对象的类型用isinstance还是type好？
class A(object):
    pass


class B(A):
    def __len__(self):
        return 0


b = B()
print(isinstance(b, B))  # True
print(isinstance(b, A))  # True
from collections.abc import Sized

print(isinstance(b, Sized))  # True
# isinstance()判断一个对象是否属于给定类型，除了会判断它属于自身类，还可以判断它属于继承链中的某个类型
# 另外，如果它实现了规定的协议，那么也可以判断它属于某种类型，例如内置的抽象基类
print(type(b) is B)  # True
print(type(b) is A)  # False
print(type(b) is Sized)  # False
# type()返回对象所属的类对象，再使用is判断返回的类对象和另一个对象是否是同一个，判断的结果不完善
# 如果用==去判断，则比较的是它们的类名

# issubclass
# 检查一个类对象的父类是否是指定的
print(issubclass(list, object))  # True list类继承自object类
print(issubclass(list, type))   # False list类对象由type类生成，

