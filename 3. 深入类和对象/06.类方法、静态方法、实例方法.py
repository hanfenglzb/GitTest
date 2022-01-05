class A(object):
    def __init__(self, num: int):
        self.num = num

    def a():
        # 会报错，但是语法没问题
        # 通过类去调用的时候，是不会自动传递任何参数的，因为
        print("类中定义的方法")

    def b(self):
        print(self.__name__)

    @classmethod
    def from_string(cls, num: str):
        return cls(
            num=int(num)
        )

    @staticmethod
    def d():
        print("静态方法")


