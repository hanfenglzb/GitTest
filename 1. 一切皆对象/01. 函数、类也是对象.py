# 函数和类都是对象，是python中的一等公民
# 1、可以赋值给一个变量
# 2、可以添加到数据结构中（dict、list、tuple、set等）
# 3、可以作为参数传递给函数
# 4、可以作为函数的返回值
# 5、可以表示的匿名字面量
# 6、在运行时构造

# 1、可以赋值给一个变量
def func(name="aaa"):
    print(name)


class Person:
    def __init__(self):
        print("test class")


# 函数的调用形式: function_object()
# 定义的func只是函数的名称，指向函数对象，将该名称赋值给另一个变量，就和将变量a赋值给变量b一样，b最终指向的是a代表的那个对象
my_func = func
my_func(name="test func")
# 所以匿名函数可以直接赋值给一个变量
lambda_func = lambda i: i + 1
print(lambda_func(10))

# 类也是一样
my_class = Person
my_class()

# 2、可以添加到数据结构中
obj_list = list()
obj_list.append(func)
obj_list.append(Person)
for item in obj_list:
    print(item())

# 3、可以作为参数传递给函数
# map、reduce、filter、sorted、zip
# 4、可以作为函数的返回值
# 装饰器、闭包
