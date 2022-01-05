def decorator(func):
    def wrapper(*args, **kwargs):
        print("...")
        return func(*args, **kwargs)

    return wrapper


@decorator
def add(a, b):
    return a + b


add(1, 2)


# @decorator 语法糖等价于
# add = decorator(add)
# wrapper = decorator(add) # 传递函数对象，返回一个被装饰过的函数对象
# add = wrapper
# add()


def decorator_fac(active=False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if active:
                print("...")
            else:
                print("。。。")
            return func(*args, **kwargs)

        return wrapper

    return decorator


@decorator_fac()
def sub(a, b):
    return a - b


sub(1, 2)

# @decorator(*args, **kwargs) 实际上是调用了装饰器工厂方法，返回了装饰器函数
# add = decorator_fac(*args, **kwargs)(add)
# decorator = decorator_fac(*args, **kwargs)
# wrapper = decorator(add)
# add = wrapper
# add()


class Decorator(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("...")
        return self.func(*args, **kwargs)


@Decorator
def mul(a, b):
    return a * b


mul(2, 3)

# mul = Decorator(mul)
# instance = Decorator(mul)
# mul = instance
# mul()


class DecoratorFac(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print(self.name)
            return func(*args, **kwargs)
        return wrapper


@DecoratorFac(name="aaa")
def div(a, b):
    return a / b


div(5, 2)

# @DecoratorFac()
# decorator = DecoratorFac(name="aaa")
# div = decorator(div)
