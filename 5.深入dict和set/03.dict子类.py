# 不建议继承原生的list和dict类
class NewDict(dict):
    def __setitem__(self, key, value):
        # 这里借用字典的__setitem__()来重写，因为该方法现在被重写了，所以需要通过super()获取
        super().__setitem__(key, value * 2)


new_dict = NewDict(a=1)
print(new_dict)  # {'a': 1} __setitem__()方法并没有生效，因为它仅在切片赋值时调用，而通过dict类直接新建字典时，内部直接是通过C语言实现的
new_dict["a"] = 1
print(new_dict)  # {'a': 2} __setitem__()方法生效了
# 不会覆盖所有操作


# 最好继承collections下的UserList、UserDict
from collections import UserDict


class NewDict1(UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, value * 2)


new_dict1 = NewDict1(a=1)
print(new_dict1)
new_dict1["a"] = 1
print(new_dict1)