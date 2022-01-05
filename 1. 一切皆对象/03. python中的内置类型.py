# ### 对象的三个特征 ###
# 1、身份（内存地址）
# 2、类型
# 3、值
#   不可变对象（值不可被改变）
#   可变对象（值可以被改变）

a = 1
# 1、身份
print(id(a))
# 2、类型
print(type(a))
# 3、值

# ### 内置类型 ###
# None
# 在解释器启动时会生成一个None对象，None对象在全局唯一
a = None
b = None


def func(c=None):
    print(a is b)
    print(a is c)


func()

# 数值类型
# int
# float
# complex（复数）
# bool

# 迭代类型
# 生成器、迭代器

# 序列类型
# str
# list
# tuple
# range
# array
# bytes（字节串）、bytearray（字节数组）、memoryview（二进制序列）

# 映射类型
# dict

# 集合类型
# set
# frozenset（不可变集合）

# 上下文管理类型
# with

# 其他类型
# 模块类型
# class和实例
# 函数类型
# 方法类型
# 代码类型
# object对象
# type类型
# ellipsis类型 省略号，用的最多的就是numpy，被重写为一种切片方式
# notimplemented类型
