# 读取大文件
def read(f_obj, size=1024 * 10):
    while True:
        content = f_obj.read(size)
        if not content:
            break
        yield content


with open("a.txt") as f:
    print("yield")
    for text in read(f):
        print(text)


# 按行读取(\n)
def readline(f_obj):
    while True:
        content = f_obj.readline()
        if not content:
            break
        yield content


with open("a.txt") as f:
    print("yield line")
    for text in readline(f):
        print(text)


# 如果要读取一个大文件，以"\n"分隔每一行，可以通过readline()；而如果需要按指定的分隔符读取文件，如./。等去读取每一句
# 没有相应的函数，这个时候需要自定义读取逻辑
def read_sep(f_obj, sep, size=1024 * 10):
    buf = ""    # 缓存，每次读取出的内容要进行处理，
    while True:
        content = f_obj.read(size)  # 从文件中读取出指定长度的字符串
        while sep in buf:
            # 如果buf中存在sep，则读取出sep的位置
            pos = buf.index(sep)
            # yield按sep分隔的一段文本
            yield buf[:pos]
            # 跳过sep，剩下的文本接着按这样的逻辑处理，直到剩下的文本中没有sep
            buf = buf[pos + len(sep):]
        # 将剩下的文本拼接到下一次读取的内容中
        # 因为这段文本的内容并不一定是完整的一段，还要接着下一次读取的内容去分割出完整的一段文本
        buf += content
        if not content:
            # 当content为空串，说明读取到文件末尾了
            # 这个时候buf不一定是空的，还可能剩下最后一句，所以也要yield这段文本
            if buf:
                yield buf
            break


with open("a.txt") as f:
    print("yield sep")
    for text in read_sep(f, "."):
        print(text)


def read_sep1(f_obj, sep, size=1024 * 10):
    buf = ""
    while True:
        content = f_obj.read(size)
        index = 0
        while True:
            try:
                # 只适用sep为单字符的情况，逐个字符对比
                # 如果sep是多个字符，每次切片获取的字符串都可能有部分和后面获取的字符串组成一个sep
                t = content[index]
            except IndexError:
                break
            else:
                if t == sep:
                    yield buf
                    buf = ""
                else:
                    buf += t
                index += 1
        if not content:
            if buf:
                yield buf
            break


print("yield sep one by one char")
with open("a.txt") as f:
    for text in read_sep1(f, "."):
        print(text)


def read_sep2(f_obj, sep, size=10):
    buf = ""  # 待处理的文本
    _text = ""  # 处理完毕的一句文本
    sep_size = len(sep)  # 分隔符长度
    while True:
        content = f_obj.read(size)  # 读取size长度的一段文本
        if not content:  # content为空，说明已经读取到文件最后
            yield _text + buf   # 当buf为最后一次切片时，长度小于sep_size，跳出了循环,导致_text没有加上这些文本
            break
        buf += content  # 每次将buf和content拼接
        index = 0
        while True:
            slice_text = buf[index:index + sep_size]  # 从buf中切出sep长的字符
            # 如果切出来的字符数少于sep，说明到了buf的最后面
            if len(slice_text) < sep_size:
                buf = slice_text
                break
            else:
                # 如果切出来分隔符，则说明获取到了一句文本，生成它并重新置空_text
                if slice_text == sep:
                    yield _text
                    _text = ""
                    index += sep_size     # 跳过分隔符
                    continue    # 跳过index += 1
                else:
                    # 如果不是，则将一个字符加到_text
                    _text += buf[index: index + 1]
            index += 1


print("yield sep multi char")
with open("a.txt") as f:
    for text in read_sep2(f, "{|}"):
        print(text)
