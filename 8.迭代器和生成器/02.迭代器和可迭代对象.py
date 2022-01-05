from collections.abc import Iterator, Iterable

a = [1, 2]
iterator = iter(a)
print(isinstance(a, Iterable))
print(isinstance(iterator, Iterator))


# 迭代器
# 实现了__iter__和__next__的对象
# 可迭代对象
# 实现了__iter__的对象，如果实现了__getitem__，可以从0开始顺序索引，也是可迭代对象

# __iter__方法
# 返回一个Iterator对象
# __next__方法
# 获取容器中下一个元素返回，当所有元素获取完毕，抛出一个StopIteration


class User:
    def __init__(self, users):
        self.users = users

    def __getitem__(self, item):
        return self.users[item]


# iter():
# 如果对象实现了__iter__()，调用该方法返回一个Iterator
# 如果没有实现，则尝试调用__getitem__()，并自动生成一个Iterator，尝试从0开始按顺序进行索引访问
# 如果都没有实现，抛出TypeError: xxx object is not iterable
# next():
# 调用迭代器对象中的__next__()，不断获取可迭代对象的下一个元素，直到抛出StopIteration异常

users = User(["aaa", "bbb", "ccc"])
for user in users:
    print(user)
# for循环会调用iter()，iter()调用可迭代对象的__iter__()，获取一个迭代器对象，然后调用next(iter_obj)，next()会
# 调用迭代器的__next__，不断的获取下一个元素，当没有元素了，处理抛出的StopIteration异常，释放迭代器，结束迭代。
# while循环模拟for循环
user_iter = iter(users)
while True:
    try:
        print(next(user_iter))
    except StopIteration:
        del user_iter
        break


class CompanyIterator:
    def __init__(self, employees):
        self.employees = employees
        self.index = 0

    def __iter__(self):
        return self  # 标准的协议中，迭代器也需要实现__iter__，返回迭代器自身，使迭代器自身也是可迭代对象

    def __next__(self):
        try:
            value = self.employees[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return value


class Company:
    def __init__(self, employees):
        self.employees = employees

    def __iter__(self):
        return CompanyIterator(self.employees)


for employee in Company(["111", "222", "333"]):
    print(employee)


# 总结
# 迭代器
# 实现__next__方法，就是一个迭代器，标准的迭代协议中迭代器还需要实现__iter__方法，返回迭代器对象自身，
# 这样迭代器自身也成为一个可迭代对象。
# 可迭代对象
# 实现__iter__方法，返回一个迭代器，就是一个可迭代对象；如果没有实现__iter__方法，那么实现了__getitem__方法也可以，
# 因为在进行迭代的时候，iter()也会尝试调用__getitem__，生成一个迭代器返回。
# 可迭代对象中也可以实现__next__方法，使可迭代对象自身成为迭代器，但是最好不要这样做，而是再实现一个迭代器，
# 在迭代器中去实现__next__方法
