# 插入排序
# 遍历数据，对遍历到的这个数据逐个跟前面的进行比较，找到它合适的位置
# 怎么找合适的位置？
# 跟前面的逐个进行比较，如果前面的比它大，就把前面那个往后移动一个位置，但是这个时候并不往空出来的那个位置插，
# 重复这个过程，直到它比前面的数据大，说明它找到合适的位置了（比它大的后一位），然后才把它插到这个位置上。
import random


def insertion_sort(arr):
    n = len(arr)
    for i in range(n):  # 每一个都要执行插入的过程，最后面那个也一样，所以是遍历n次
        insert_num = arr[i]  # 保存一下要插入的数据
        previous_index = i - 1  # 要插入的数据的前一个位置
        while previous_index >= 0:  # 跟前面的数据逐一比较，如果一直没比较出来，那么一直要比到第一个
            if insert_num > arr[previous_index]:  # 如果待插入的数据比前一个数据大，说明应该插入到这个位置
                break
            # 否则，将前一个数据往后挪一位，但是不插入，接着跟前面的比较
            arr[previous_index + 1] = arr[previous_index]
            previous_index -= 1
        # 找到应该插入的位置后，插入数据
        arr[previous_index + 1] = insert_num
    return arr


def insertion_sort1(arr):
    n = len(arr)
    for i in range(n):
        insert_num = arr[i]
        previous_index = i - 1
        while previous_index >= 0 and insert_num < arr[previous_index]:
            arr[previous_index + 1] = arr[previous_index]
            previous_index -= 1
        arr[previous_index + 1] = insert_num
    return arr


arr = [random.randint(0, 100) for _ in range(10)]
print(insertion_sort(arr))
print(insertion_sort1(arr))


# 时间复杂度：
# #   最好情况：O(n) 当数据是有序的，那么内层循环找插入位置时只需要比较一次就退出
# #   最坏情况：O(n^2) 当数据是反序时，所有数据都要逐个找插入位置，并且每次找位置时内层循环都会达到最大次数
# #   平均：O(n^2)
# 空间复杂度：O(1) 只用了有限的几个变量
# 排序方式：原地排序（in-place），还是在原来的序列中进行数据的交换
# 稳定性：稳定 相同的数据排完还是保持原来的顺序
