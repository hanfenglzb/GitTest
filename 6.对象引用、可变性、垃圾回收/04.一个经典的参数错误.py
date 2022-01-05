def add(a, b):
    a += b
    return a


# 当参数为整数
a = 1
b = 2
c = add(a, b)
print(c, a, b)
# 当参数为列表
a = [1, 2]
b = [3, 4]
c = add(a, b)
print(c, a, b)
# 当参数为元组
a = (1, 2)
b = (3, 4)
c = add(a, b)
print(c, a, b)


class Company(object):
    # def __init__(self, name, staffs=None):
    #     if staffs is None:
    #         staffs = []
    #     self.name = name
    #     self.staffs = staffs
    def __init__(self, name, staffs=[]):
        self.name = name
        self.staffs = staffs

    def add(self, staff_name):
        self.staffs.append(staff_name)

    def remove(self, staff_name):
        self.staffs.remove(staff_name)


print(Company.__init__.__defaults__[0], id(Company.__init__.__defaults__[0]))
com1 = Company("com1", ["a", "b"])
com1.add("c")
com1.remove("a")
print(com1.staffs, id(com1.staffs))

com2 = Company("com2")
com2.add("a2")
print(com2.staffs, id(com2.staffs))

com3 = Company("com3")
com3.add("a3")
print(com3.staffs, id(com3.staffs))


# 函数的默认参数会被设置为函数对象的__defaults__属性（func.__defaults__），为一个元组，按默认参数的顺序存储
# 不管调用多少次函数，如果涉及使用默认参数，用的都是同一个（__defaults__是该函数对象的实例属性）
# 当这个默认参数为不可变对象时，不会有问题，但是当它是一个不可变对象时，问题就出现了
# 因为每一次调用函数，使用的都是这个默认参数，以列表为例，当有一次调用时使用了这个默认列表并向里面添加了数据，这实际上
# 是修改了__defaults__属性，下一次调用函数时也用这个默认列表的话，这个默认列表已经不是定义时的默认列表了。
