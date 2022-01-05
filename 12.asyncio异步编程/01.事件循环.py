import asyncio
import time
from functools import partial


# 单线程的异步执行
# 在同步的模式下，碰到耗时操作、IO操作，CPU只能等待，直到完成后再接着运行
# 可以将耗时的任务新开线程或进程运行，但是一台计算机能开启的线程和进程都是有限的，当并发数量很大，这种同步的方式肯定不满足
# 异步就是在碰到耗时或IO操作的时候，暂停该任务的运行，切换到其他任务的运行，在单线程模式下也能保持碰到IO操作时不阻塞线程的运行，
# 具体的实现就是通过select/poll/epoll等方式，从操作系统层面获取已经完成的事件，恢复任务的执行。
async def get_html(url):
    print("start get html")
    await asyncio.sleep(2)
    print("end get url")


async def get_html1(url):
    print("start get html")
    await asyncio.sleep(1)
    return url


def callback(future):
    print(future)
    print("send email")


def callback1(arg1, future):
    print(arg1, future)
    print("send email")


if __name__ == '__main__':
    start_time = time.time()
    loop = asyncio.get_event_loop()
    tasks = [get_html("https://www.baidu.com") for _ in range(5)]
    # loop.run_until_complete(get_html("https://www.baidu.com"))
    loop.run_until_complete(asyncio.wait(tasks))
    end_time = time.time()
    print(end_time - start_time)
    # 获取协程的返回值1
    future = asyncio.ensure_future(get_html1("https://www.baidu.com"))
    loop.run_until_complete(future)
    print(future.result())
    # 获取协程的返回值2
    task = loop.create_task(get_html1("https://www.baidu.com"))
    loop.run_until_complete(task)
    print(task.result())
    # 给协程添加回调函数，协程执行完成之后将会调用该回调函数
    task = loop.create_task(get_html1("https://www.baidu.com"))
    task.add_done_callback(callback)
    loop.run_until_complete(task)
    print(task.result())
    # 如果回调函数中需要其他参数，而add_done_callback只会给自定义回调函数传递一个值，如何传递其他参数？
    # 1.可以使用偏函数functools.partial（需要注意参数的顺序）
    # 2.函数对象有defaults属性，直接操作设置该属性
    task = loop.create_task(get_html1("https://www.baidu.com"))
    task.add_done_callback(partial(callback1, "回调参数1"))
    loop.run_until_complete(task)
    print(task.result())

    # wait和gather
    # wait类似ThreadExecutorPool中的wait，放入协程函数组成的可迭代对象，在指定的事件之后返回一个协程
    # gather
    # 同样放入协程函数组成的可迭代对象，还可以收集分组
    task1 = [get_html("https://www.baidu.com") for _ in range(2)]
    task2 = [get_html("https://www.imooc.com") for _ in range(2)]
    group1 = asyncio.gather(*task1)
    group2 = asyncio.gather(*task2)
    loop.run_until_complete(asyncio.gather(group1, group2))
