# 列表推导式、字典推导式、集合推导式、生成器推导式
# 列表推导式
# 1.基本推导式
nums1 = []
for i in range(1, 10):
    nums1.append(i * i)
nums2 = [i * i for i in range(1, 10)]
print(nums1, nums2)

# 2.带推导条件的推导式
nums1 = []
for i in range(1, 10):
    if i % 3 == 0:
        nums1.append(i * i)
nums2 = [i * i for i in range(1, 10) if i % 3 == 0]
print(nums1, nums2)

# 3.推导式中应用条件分支语句(...if...else...: 条件运算符)
nums1 = []
for i in range(1, 10):
    if i % 3 == 0:
        nums1.append(i * i)
    else:
        nums1.append(i)
nums2 = [i * i if i % 3 == 0 else i for i in range(1, 10)]
print(nums1, nums2)
# 一个完整的推导式语法：[推导表达式分支1 if 条件表达式 else 推导表达式分支2 for 标识符 in 序列 if 推导条件]
# 注意当if处于不同位置的作用：
# 当处于循环右侧时，根据推导条件筛选出元素
# 当处于循环左侧时，if并不是单独存在的，实际上是<...if...else...>条件表达式
#   对上一个if筛选出的元素再次进行条件控制，决定应该怎么生成值
# 两处if都可以省略
# 比如：
print([i * i if i % 3 == 0 else i for i in range(1, 10) if i < 10])
# 从range(1, 10)中推导
# 只要小于10的元素
# 这些小于10的元素如果能被3整除，则生成它们的平方，否则生成本身

# 4.推导式中应用函数
# 推导式中如果某个部分的逻辑比较复杂，则可以使用函数
# 推导条件、推导表达式、分支语句的条件
# 例；在推导条件中使用函数
nums1 = []


def is_prime(num):
    if num == 1:
        return False
    for i in range(2, num):
        if num % i == 0:
            return False
    else:
        return True


for i in range(1, 10):
    if is_prime(i):
        nums1.append(i)
nums2 = [i for i in range(1, 10) if is_prime(i)]
print(nums1, nums2)

# 5.嵌套推导式
# [推导表达式分支1 if 条件表达式 else 推导表达式分支2 for 标识符1 in 序列1 if 推导条件1 for 标识符2 in 序列2 if 推导条件2 ...]
# 几个for循环 + if推导条件（可以省略）就是几层for循环，比如两个for循环，则为两层嵌套如下：
nums1 = []
for year in range(2016, 2021):
    for mouth in range(1, 13):
        nums1.append((year, mouth))
nums2 = [(year, mouth) for year in range(2016, 2021) for mouth in range(1, 13)]
print(nums1, nums2)
# 每个for循环都加上推导条件
nums1 = []
for year in range(2016, 2021):
    for mouth in range(1, 13):
        nums1.append((year, mouth))
nums2 = [(year, mouth) for year in range(2016, 2021) if year % 2 == 0 for mouth in range(1, 13) if mouth < 3]
print(nums2)

# 以上语法下面几种推导式一样可用
# 生成器推导式
# 使用()即可

# 字典推导式
# 使用{}
# 推导表达式为key:value形式
nums_dict1 = {}
for i in range(1, 10):
    nums_dict1[i] = i * i
nums_dict2 = {i: i * i for i in range(1, 10)}
print(nums_dict1, nums_dict2)


score = {'aa': 59, 'bb': 87, 'cc': 78, 'dd': 100, 'ee': 90}
# key-value互换
print({value: key for key, value in score.items()})
# 按分数排序
print({key: value for key, value in sorted(score.items(), key=lambda item: item[1])})


# 集合推导式
# 使用{}
# 去掉重复值
print({i for i in "advanced python"})
