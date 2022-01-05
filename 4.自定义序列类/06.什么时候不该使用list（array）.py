# 类似list的可变序列有哪些：array、deque
# array和list的区别
# array只能存放同种类型的数据（且必须是指定的几种类型之一，实例化array对象时指定）
import array
a = array.array("i")
a.append(1)
a.append(2)
print(a)
