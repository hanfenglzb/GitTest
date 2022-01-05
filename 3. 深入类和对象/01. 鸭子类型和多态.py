# ### 多态 ###
# 不同对象做相同操作的时候会有不同的体现（为不同数据类型的实体提供统一接口）
# 常见的类别有以下三种
# 1、特设多态（对不同的类型定义一个共同接口）
#     多态函数有多种不同的实现，根据不同的实参去调用相应版本的函数，也就是说特设多态仅支持有限数量的不同类型。
#     特设多态是一种针对特定问题的解决方案，具体的情形有：函数重载、运算符重载
#     比如说，不同类型的对象做 + 运算：
#             1 + 2 = 3  （整型与整型）
#             3.14 + 0.00159 = 3.14159 （浮点型与浮点型）
#             1 + 2.7 = 3.7  （整型与浮点型）
#             "pyt" + "hon" = "python" （字符串与字符串）
#             [1, 2, 3] + [4, 5, 6] = [1, 2, 3, 4, 5, 6] （列表与列表）
#         第一种情形，需要实现两个整型之间的add函数，返回一个整型数值
#         第二、三种情形，需要实现两个浮点型之间的add函数，返回一个浮点型数值（其中第三种情形还需要隐式类型转换，它也是一种多态的形式，叫做强迫多态）
#         第四种情形，需要实现两个字符串类型之间的add函数，返回连接在一起的新字符串
#         第五种情形，需要实现两个列表类型之间的add函数，返回连接在一起的新列表
#         运算符 + 号好像通用的工作在不同类型上，但实际上针对不同类型，add函数会有多个不同的实现
#     多态体现为：不同类型的对象做 + 运算时都是调用add()函数,但得到的结果却并不相同（为不同的数据类型提供了统一的 + 操作）
# 2、参数多态（泛型编程）
#     声明与定义函数、复合类型、变量时不指定其具体的类型，而把这部分类型作为参数使用，使得该定义对各种具体类型都适用
#     这个参数只是一个泛指，它不要求必须传递某个类型，但是传递进来的数据类型需要是可以正确运行的
#     应用的地方有C++模板、Java泛型等
#     多态体现为：不同的数据类型对象在被传递进同一个参数时会有不同的表现（为不同的数据类型提供了统一的参数传递操作）
#
#
# 3、子类型多态（一般在面向对象语言中说的多态就是子类型多态）
#     父类对象可以使用的地方，它的子类对象可以无条件的使用

class Animal(object):
    def say(self):
        print("I am an animal")


class Cat(Animal):
    def say(self):
        print("I am a cat")


class Dog(Animal):
    def say(self):
        print("I am a dog")


class Duck(Animal):
    def say(self):
        print("I am a duck")


def animal_say(animal: Animal):
    if isinstance(animal, Animal):
        animal.say()
    else:
        raise TypeError


print(" 继承方式 ".center(20, "#"))
animal_say(animal=Cat())
animal_say(animal=Dog())
animal_say(animal=Duck())


# Java实现多态
# class Animal:
#     def say(self):
#         print("I am an animal")
#
#
# class Cat(Animal):
#     def say(self):
#         print("I am a cat")
#
#
# Animal cat = Cat()  # 指定cat的类型为Animal并通过Cat类进行实例化
# cat.say()

# 通过继承实现多态要求子类必须实现父类的方法
# 上面使用继承的方式模拟实现静态语言的子类型多态，为什么是模拟呢？
#     对于静态语言来说（比如Java），在animal_say函数中声明了参数类型为Animal，那么它可以传递的对象就被限定为Animal或其子类，否则编译时就会报错
#     在Python中，变量不会绑定具体的类型，虽然参数是animal，但这个参数名是什么对象都可以，animal.say()
#     调用的是animal这个变量所引用的对象中的say()方法。
#     在函数里面使用isinstance()函数对传入的类型进行限制，屏蔽Python变量的特性，可以起到静态语言的效果。


# ### 鸭子类型 ###
# 当看到一只鸟走起来像鸭子、游泳起来像鸭子、叫起来也像鸭子，那么这只鸟就可以被称为鸭子。
# 鸭子类型关注的是对象的行为（也就是它能干什么），不管它是什么类型的对象
# 只要它具有在某个使用环境中要求的属性或方法，那么它就能该环境中使用
class Cat(object):
    def say(self):
        print("I am a cat")


class Dog(object):
    def say(self):
        print("I am a dog")


class Duck(object):
    def say(self):
        print("I am a duck")


def animal_say(animal):
    animal.say()


print(" 非继承方式 ".center(20, "#"))
animal_say(animal=Cat())
animal_say(animal=Dog())
animal_say(animal=Duck())


# 可以看到上面各个类之间并没有继承关系，但是鸭子类型在不使用继承的方式下同样实现了多态，唯一的要求就是不同的对象必须都定义了say()方法
# 取决于你需要哪个像鸭子的行为的子集来使用
# 比如列表的extend方法，它要求传入一个可迭代对象，也就是说，只要传入的对象实现了__iter__()方法即可
# 但是在没有鸭子类型的语言中，例如java，必须传入同种类型或其子类的对象，也就是一个列表才行。
# Python的魔术方法就是鸭子类型最好的应用，只要不同对象实现了相同的魔术方法，那它们就可以在特定语法或操作中使用。
# 因为鸭子类型的存在，在Python中判断一个类或者对象属于什么类型，有什么特性，只看它实现了哪些魔术方法或其他方法、属性等。
# 而Java中的对象在生成时就需要指定它的类型。
a = ["a", "b"]
b = ["c", "d"]
a.extend(b)
print(a)
name_tuple = ("e", "f")
name_set = {"g", "h"}
a.extend(name_tuple)
print(a)
a.extend(name_set)
print(a)


# 动态类型和静态类型的区别


# 参考链接
# https://www.liaoxuefeng.com/wiki/1016959663602400/1017497232674368
# https://www.jianshu.com/p/650485b78d11
# https://zh.wikipedia.org/wiki/%E9%B8%AD%E5%AD%90%E7%B1%BB%E5%9E%8B
# https://zh.wikipedia.org/wiki/%E5%A4%9A%E6%80%81_(%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A7%91%E5%AD%A6)
