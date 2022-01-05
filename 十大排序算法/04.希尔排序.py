# 希尔排序是插入排序的一种改进
# 基于插入排序以下两点性质改进：
# 1.插入排序在对几乎已经排好序的数据操作时，效率高，可达到类似线性排序的效率
#   （在内层循环中跟前面数据的比较很快完成，内层循环执行的次数少）
# 2.插入排序是低效的，因为每次