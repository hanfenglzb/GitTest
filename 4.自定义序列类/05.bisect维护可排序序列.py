# bisect模块
# 用来处理已排序的序列，使其在做完操作后仍然保持排序状态（升序）
# bisect模块使用二分查找算法

import bisect

# insort()
# insort = insort_right
# 向序列中插入x，并保持序列处于排序状态(它是默认这个序列已经处于一个排好序的状态)
# a = [6, 4, 2, 8, 9]
# bisect.insort(a, 2)
# print(a)
# -> [6, 4, 2, 2, 8, 9]
# 如果x已经在序列中，那么往最右边一个x的后面位置插入
int_list = []
bisect.insort(int_list, 6)
bisect.insort(int_list, 1)
bisect.insort(int_list, 5)
bisect.insort(int_list, 4)
bisect.insort(int_list, 2)
print(int_list)

# insort_left()
# 如果x已经在序列中，那么往最左边一个x的前面位置插入

# bisect()
# bisect = bisect_right()
# 获取一个元素应该插入的位置(右插，索引值从0开始)
location = bisect.bisect(int_list, 3)
print(location)
# bisect_left()
# 获取一个元素应该插入的位置(左插，索引值从0开始)
location = bisect.bisect_left(int_list, 3)
print(location)

# 左插和右插的区别在哪里？
# 1. 1 和 1.0
# 1和1.0的值是相等的，如果想要保持1在前，这时应该用左插
# 2. 学生成绩的等级是一个范围
# A: 90-100
# B: 75-89
# C: 60-74
# D: <60
# 90分和91分，都属于A等级，但是谁应该在前面呢，显然90应该保持在91前面
# {
#     "A": [90, 91]
# }

