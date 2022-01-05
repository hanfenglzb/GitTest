# collections模块：内置类型外的其他容器类型
# collections.abc模块：与容器类型相关的抽象基类
from collections.abc import Sequence, MutableSequence
# Sequence：不可变序列抽象基类
# MutableSequence：可变序列抽象基类
# 这些内置类型的抽象基类更多的是用来查看需要定义哪些魔术方法（或其他方法）使其成为自定义的该类型
# 在自定义这些类型的时候，可以继承这些抽象基类，保证不会遗漏某个必须的方法
