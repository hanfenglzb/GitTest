# 生成器函数：函数中有yield关键字，函数就不再是一个普通的函数

def generator_func():
    yield 1
    yield 2


def func():
    return 1


gen = generator_func()
res = func()
print(gen)  # 调用生成器函数返回一个生成器对象，在Python进行编译字节码的时候就生成了
print(res)
# 生成器对象实现了迭代协议
for value in gen:
    print(value)


# 通过生成器可以实现惰性求值（延迟求值）
# 斐波那契数列
# 1 1 2 3 5 8 ...
print("fibonacci")


def fib(count):
    # 返回指定位数
    if count <= 2:
        return 1
    return fib(count - 1) + fib(count - 2)


print(fib(3))
print("fibonacci")


def fibonacci(count):
    # 返回指定个数的数列
    a, b = 0, 1
    for _ in range(count):
        yield b
        a, b = b, a + b


for i in fibonacci(10):
    print(i)
