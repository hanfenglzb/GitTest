class Company(object):
    def __init__(self, employee: list):
        self.employee = employee

    def __getitem__(self, item):
        return self.employee[item]


company = Company(["a", "b", "c"])
# 想要遍历company实例中的员工，在不实现任何魔法函数的情况下，需要先获取到属性
for em in company.employee:
    print(em)
# 通过魔术方法实现
# __getitem__方法，实现对象的切片操作  company[i] == type(company).__getitem__(x, i)
# 遍历company对象，for循环会看对象是否是一个迭代器（即是否实现了__iter__方法）
# 若没有则寻找是否实现__getitem__()方法，参数从0开始传递给__getitem__()，
# 直到抛出异常，循环结束；如果没有抛出异常，则循环不结束
for em in company:
    print(em)
print(company[0: 3])


# 魔术方法（特殊方法）
# 魔术方法是在类中已经预定义的一些方法，以双下划线（__）开头和结尾
# 一个类可以通过定义具有特殊名称的方法来实现由特殊语法所引发的特定操作，或者说这些语法或操作要求对象必须定义了对应的魔术方法
# 例如list类中实现了__getitem__()方法，所以列表支持切片语法，还有像内置函数、对象比较等操作，最终都是调用类中实现的魔术方法。
# 除非有说明例外情况，否则在类中没有定义适当的魔术方法的情况下，其实例对象尝试执行一种操作将引发一个异常，通常是AttributeError或TypeError
# 魔术方法可以增强类的功能，但一个对象应该在确实需要支持某些语法的时候才去定义相应的魔术方法，定义的魔术方法对对象来说应该是有意义的