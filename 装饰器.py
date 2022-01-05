def _func(a, b):
    return a + b


def wrapper_func(a, b):
    print("装饰过的新函数")
    return _func(a, b)


def wrapper1_func(*args, **kwargs):
    print("非固定参数")
    return _func(*args, **kwargs)


def common_wrapper_func(func, *args, **kwargs):
    print("通用的装饰函数")
    return func(*args, **kwargs)


# 闭包实现装饰器
def decorator(func):
    def wrapper(*args, **kwargs):
        print("装饰器")
        return func(*args, **kwargs)

    return wrapper


@decorator
# add = decorator(add)
def add(a, b):
    return a + b


def decorator_factory(a=1, b=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print("带参数的装饰器")
            print(a, b)
            return func(*args, **kwargs)

        return wrapper

    return decorator


@decorator_factory()  # decorator = decorator_factory(a=1, b=2)  返回装饰器函数
# mul = decorator(mul)  返回被装饰过的函数
def mul(a, b):
    return a * b


class Decorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("类装饰器")
        return self.func(*args, **kwargs)


@Decorator
# sub = Decorator(sub)
def sub(a, b):
    return a - b


class DecoratorFactory:
    def __init__(self, a=1, b=2):
        self.a = a
        self.b = b

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print("带参数的类装饰器")
            return func(*args, **kwargs)

        return wrapper


@DecoratorFactory()  # decorator = DecoratorFactory(a=1, b=2)
# div = decorator(div)
def div(a, b):
    if b == 0:
        raise ValueError("除数不能为0")
    return a / b


class A:
    def a(self, func):
        def wrapper(*args, **kwargs):
            print("类装饰器-普通方法")
            return func(*args, **kwargs)

        return wrapper

    def b(self, a=1, b=2):
        def decorator(func):
            def wrapper(*args, **kwargs):
                print(a, b)
                print("带参数的类装饰器-普通方法")
                return func(*args, **kwargs)

            return wrapper

        return decorator


@A().a
def pow(a, b):
    return a ** b


@A().b()
def mod(a, b):
    return a % b


print(mod(2, 3))
