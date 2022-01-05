# 字符串表示
# __str__: 在使用str()函数的时候调用
# __repr__: 在使用repr()函数的时候调用

class Company(object):
    def __init__(self, employee: list):
        self.employee = employee

    def __str__(self):
        return "、".join(self.employee)

    def __repr__(self):
        return "、".join(self.employee)


company = Company(["a", "b", "c"])
print(company)          # print()函数会先调用str(company)，而str(company)会调用company对象的__str__()方法，即company.__str__()
print(repr(company))    # repr(company)会调用company.__repr__()
