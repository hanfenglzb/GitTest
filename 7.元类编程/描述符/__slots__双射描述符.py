class A:
    __slots__ = ("name", )


a = A()
a.name = "aaa"
print(a.name)
a.age = 18
print(a.age)
