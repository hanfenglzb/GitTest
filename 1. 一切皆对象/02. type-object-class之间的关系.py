# ####### 类 #######
# 类可以生成实例对象
# 类本身也是一个对象（称为类对象，也是一个实例对象）

# ####### type类 #######
# type是一个类
# 1、type类可以获取到对象的类型（也就是对象由哪个类生成的）
# 2、type类可以生成类对象
print(type(1))      # 1是int类生成的实例对象 <class 'int'>
print(type(int))    # 类也是对象，那么int类对象是什么类型的呢（谁生成了int类对象） <class 'type'>
# type -> int -> 1
print(type("abc"))  # abc是str类生成的实例对象 <class 'str'>
print(type(str))    # str类是type类生成的实例对象 <class 'type'>
# type -> str -> "abc"


# 对于自定义的类和内建类（int,float,str,list,dict等）都是一样的
class Test:
    pass


t = Test()
print(type(t))              # <class '__main__.Test'>
print(type(Test))           # <class 'type'>
# type类生成类对象，类对象再生成实例对象
# type -> class -> instance


# ####### object类 #######
# object类是最顶层的父类，所有类推到最后都是继承自object类
# 如果一个类在定义的时候没有继承任何类，则它会默认继承object类
class Student1(object):
    pass


class Student2(Student1):
    pass


# class.__bases__ 可以获取类对象的父类对象（元组形式返回 -> 因为可以继承多个父类）
print(int.__bases__)            # (<class 'object'>,)
print(str.__bases__)            # (<class 'object'>,)
print(Student1.__bases__)       # (<class 'object'>,)
print(Student2.__bases__)       # (<class '__main__.Student1'>,)
print(Student2.__bases__[0].__bases__)     # (<class 'object'>,)


# ####### type和object的关系 #######
# type类是由谁生成？继承自谁？
print(type(type))           # <class 'type'> -> type类对象由自己生成
print(type.__bases__)       # (<class 'object'>,) -> type类同样继承object类
# object类由谁生成？继承自谁？
print(object.__bases__)     # ()  -> object没有基类
print(type(object))         # <class 'type'> -> object类对象也是通过type类去生成的


# 从类继承的角度来看，所有类都继承自object类，包括type类，但不包括object自身
#   object是所有类的最顶层父类
#   object类本身则没有父类
# 从类对象的角度来看，所有类对象都由type类生成，包括object类和type类本身
#   type类生成所有类对象
#   type类也是由自己生成（一个类怎么实例化自己？通过指针实现）
