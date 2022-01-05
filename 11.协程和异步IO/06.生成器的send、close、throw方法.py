def gen_func():
    yield 1
    yield 2
    yield 3


gen = gen_func()
print(next(gen))
print(next(gen))
print(next(gen))
try:
    print(next(gen))
except StopIteration:
    print("生成器迭代完毕")


# 使用send
def gen_func1():
    res = yield 1
    print(res)
    yield 2
    yield 3


gen = gen_func1()
print(next(gen))
gen.send(10)


# send方法的参数值会成为暂停处的yield表达式的值，该例中res的值会被设置为10
# send方法必须在协程处于暂停的情况下调用，即运行碰到第一个yield语句，此时send会设置yield表达式的值
# 并且会从暂停处继续运行，直到下一个yield处生成完值之后再次暂停或者函数结束抛出StopIteration异常

# 所以在调用send方法前需要先预先激活协程（预激协程，即让协程运行到第一个yield处暂停，此时的协程成为活跃状态）
# 有两种方式：
# 1.调用一次next(gen)
# 2.调用一次gen.send(None)
# 在激活前不能通过send发送非None值，否则会抛出一个TypeError
