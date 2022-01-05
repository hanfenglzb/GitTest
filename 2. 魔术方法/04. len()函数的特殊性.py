class Company(object):
    def __init__(self, employee: list):
        self.employee = employee

    def __len__(self):
        # __len__()要求返回一个数值代表长度
        # 这里可以采用循环计数获取self.employee的个数
        # count = 0
        # for item in self.employee:
        #     count += 1
        # return count
        # 也可以直接调用len()，因为list也实现了__len__()
        return len(self.employee)
        # len(self.employee) -> self.employee.__len__()


company = Company(["a", "b", "c"])
print(len(company))     # len(obj)会调用obj.__len__()


# 没有定义__len__()
class Company1(object):
    def __init__(self, employee: list):
        self.employee = employee


company1 = Company1(["a", "b", "c"])
print(len(company1))


# Company类中定义了__len__()方法，所以可以直接对company对象调用用len()函数
# Company1类中没有定义__len__()方法，不能对company1对象调用len()函数
# 但是在读取self.employee的长度时，并不需要遍历这个列表去获取数据长度，直接使用len(self.employee)即可
# 因为list同样实现了__len__()，而且len()函数在python原生的数据结构（比如list）进行操作时，都不需要遍历，直接读取底层维护的数据即可
# 所以，尽量使用python原生的数据结构、内置函数等，解释器内部针对这些原生操作做了一些优化
