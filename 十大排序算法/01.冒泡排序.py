# 冒泡排序:
# 遍历序列，每次遍历在未排序的数据中找出最大的；
# 怎么找最大的：每次遍历时，两两比较元素大小，如果前一个比后一个大，则交换它们的顺序，直到排好
def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):  # 最后只剩下一个元素时，就没有必要再排序了，所以遍历n-1次即可
        for j in range(n - 1 - i):  # n个元素两两比较，只需要n-1次；同时，已经排序好的不需要再交换，再减去i
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def bubble_sort1(arr):
    n = len(arr)
    for i in range(n - 1):
        flag = False    # 加一个标志位，如果在一次遍历中没有发生数据顺序的交换，则表示已经排序完成
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                flag = True
        if not flag:
            return arr
    return arr

# 时间复杂度：
#   最好情况：O(n)，数据已经是正序时，只需要遍历一遍即可
#   最坏情况：O(n^2)，数据为反序时，所有数据都要交换位置
#   平均：O(n^2) 只有加了标志位才有最好情况的说法，没有标志位的话不管什么数据都要双重遍历
# 空间复杂度：O(1)，只需要有限的几个变量
# 排序方式：in-place 原地排序
# 稳定性：稳定

# 排序方式：
#   原地排序(in-place)：指排序过程中只使用常数内存，没有使用额外的内存
#   非原地排序(out-place)：指排序过程中使用了额外的内存
# 稳定性：
#   稳定：指相同的两个值的顺序在排序过后还是原先的顺序
#   不稳定：指定相同的两个值的顺序在排序过后发生了改变
