# 1.dict的key和set的value都必须是可hash的，python通过构建它们的hash表实现查找的时间复杂度为O(1) -> 数组，通过偏移量查找
# 不可变对象，都是可hash的，str、tuple、bytes、int、float、bool、frozenset、namedtuple等
# 自定义类也可以重写__hash__()方法使其实例成为可hash的
# 2.dict的内存花销大，查询速度快，空间换时间
# 3.dict的存储顺序和添加顺序有关，当后添加的key造成hash冲突时，它就不一定放在hash表的哪一处了，这跟解决hash冲突的算法有关
# 注：python3.6版本后的dict已经是顺序存储！
# 4.当hash表的数据过多，会重新分配内存，原有数据会拷贝至新的内存中，顺序有可能被打乱。
# 注：python3.6版本后的dict已经是顺序存储！

# set和dict都是通过hash表实现快速查找
