# + 运算符
a = [1, 2, 3]
b = [4, 5]
c = a + b
print("c->+", c)    # 序列通过 + 运算，会得到一个新的序列对象

# +=
a1 = [1, 2, 3]
b1 = [4, 5]
a1 += b1
print("a1->+=", a1)
# 列表类型的 += 符号会触发调用__iadd__()方法，该方法实际上是调用了extend()，extend()则循环调用append()
a1 += ("a", "b")    # +=的右值可以是任意的iterable
print("a1->+=", a1)
# 但是当序列是元组时，是没有extend()方法的，它等价于a = a + b，生成了新的元组对象
a = (1, 2)
print(id(a))
b = (3, 4)
a += b
print(a, id(a))

# extend
a2 = [1, 2, 3]
b2 = [4, 5]
a2.extend(b2)
print("a2->extend()", a2)





