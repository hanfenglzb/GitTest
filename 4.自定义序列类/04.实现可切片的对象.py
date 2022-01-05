class Group(object):
    def __init__(self, group_name: str, company_name: str, staffs: list):
        self.group_name = group_name
        self.company_name = company_name
        self.staffs = staffs

    def __len__(self):
        return len(self.staffs)

    def __reversed__(self):
        cls = type(self)
        self.staffs.reverse()
        # 可以返回一个新的对象，也可以不返回
        return cls(
            group_name=self.group_name,
            company_name=self.company_name,
            staffs=self.staffs
        )

    # 实现__getitem__()方法就可以切片
    def __getitem__(self, item):
        # return self.staffs[item]    # 简单的将它交给列表处理，返回的是一个列表
        # 如果还想返回一个Group类型呢？
        # 1.获取self的类型
        cls = type(self)  # 动态获取，尽量不要硬编码
        # cls = self.__class__
        # 2.进行切片处理
        # item传递一个int类型（索引方式）或slice类型（切片方式）
        if isinstance(item, int):
            return cls(
                group_name=self.group_name,
                company_name=self.company_name,
                staffs=[self.staffs[item]]  # 索引得到的是单个元素，而staffs要求是列表，所以重新转换为列表
            )
        elif isinstance(item, slice):
            return cls(
                group_name=self.group_name,
                company_name=self.company_name,
                staffs=self.staffs[item]
            )
        else:
            # 其他类型则抛出异常
            # 如果想要做的更完善，接着判断类型做处理
            raise TypeError

    def __iter__(self):
        return iter(self.staffs)

    def __contains__(self, item):
        return item in self.staffs


group = Group(
    "1组",
    "xxx公司",
    ["a", "b", "c"]
)
# __len__()
print(len(group))
# __getitem__()
print(group[1].staffs)
print(group[0:2].staffs)
# __reversed__()
group1 = reversed(group)
print(group1.staffs)
# __iter__()
for staff in group:
    print(staff)
# __contains__()
print("a" in group)

