class Student(object):
    def __init__(self, name, math, chinese, english):
        self.name = name
        self.math = math
        self.chinese = chinese
        self.english = english


student = Student(
    name="aaa",
    math=85,
    chinese=200,
    english="70"
)


# 类中属性应该是对外封闭的，不应该暴露给外部，通过封装的函数来获取
# 类中属性也没有做限制，可能被赋值为任何值


class Student1(object):
    def __init__(self, name, math, chinese, english):
        self._test = 1
        self.__test = 2
        self.name = name
        if 0 <= math <= 100:
            self.math = math
        else:
            raise ValueError("Valid value must be in [0, 100]")
        if 0 <= chinese <= 100:
            self.chinese = chinese
        else:
            raise ValueError("Valid value must be in [0, 100]")
        if 0 <= english <= 100:
            self.english = english
        else:
            raise ValueError("Valid value must be in [0, 100]")

    def get_math(self):
        return self.math

    def set_math(self, value):
        if 0 <= value <= 100:
            self.math = value

    def del_math(self):
        self.math = None

    ...


# 判断逻辑太多重复的代码，属性的访问、修改、删除也需要设置大量的方法
try:
    student1 = Student1(
        name="aaa",
        math=90,
        chinese=200,
        english="70"
    )
except ValueError as e:
    print("Student1: " + str(e))


class Student2(object):
    def __init__(self, name, math, chinese, english):
        self.name = name
        self.math = math
        self.chinese = chinese
        self.english = english

    @property
    def math(self):
        return self._math   # 不是在初始化的时候也可以生成

    @math.setter
    def math(self, value):
        if 0 <= value <= 100:
            self._math = value
        else:
            raise ValueError("Valid value must be in [0, 100]")

    @math.deleter
    def math(self):
        self._math = None

    def get_chinese(self):
        return self._chinese

    def set_chinese(self, value):
        if 0 <= value <= 100:
            self._chinese = value
        else:
            raise ValueError("Valid value must be in [0, 100]")

    def del_chinese(self):
        self._chinese = 0

    # 使用property()内置类也是一样的，上面的是装饰器实现及用法
    chinese = property(
        fget=get_chinese,
        fset=set_chinese,
        fdel=del_chinese,
    )


student2 = Student2(
    name="aaa",
    math=90,
    chinese=100,
    english=70
)
# 为什么在__init__方法中初始化的时候就触发了方法中的判断逻辑呢，不是应该涉及对应属性的访问，修改，删除的时候才触发吗？
# 在类中的赋值一样是赋值！而且在初始化函数中进行赋值操作的其实是属性描述符，并不是实例的基本属性

print(student2.__dict__)

