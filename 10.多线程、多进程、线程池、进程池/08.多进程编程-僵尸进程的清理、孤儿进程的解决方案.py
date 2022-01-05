# _cleanup()
#   -> .../Lib/multiprocessing/process/_cleanup()
# def _cleanup():
#     # check for processes which have finished
#     for p in list(_children):
#         if p._popen.poll() is not None:
#             _children.discard(p)

# process对象的_popen.poll() -> Popen对象-进程文件指针
#   -> .../Lib/multiprocessing/[popen_fork|popen_spawn_win32|...]/Popen().poll()

# Python的父进程会自动清理僵尸进程，
# 在multiprocessing下的所有函数或方法中，如果调用了_cleanup()或Popen()._popen/wait()等方法，那么会自动清理僵尸进程。
# 如:
#   父进程正常退出的时候会进行清理。
#   调用Process()对象的一些方法的时候：
#       start(): 启动新进程
#       join(): 父进程阻塞等待子进程退出
#       is_active(): 查看进程是否存活
#       close(): 关闭进程对象
#       exitcode: 进程退出状态码
#       __repr__(): 打印进程对象的时候
#       terminate(): signal.SIGTERM信号杀死进程
#       kill: signal.SIGKILL信号杀死进程
#   multiprocessing模块函数
#       active_children(): 获取当前进程所有存活的子进程的时候

# 所以Python的多进程一般不需要考虑清理僵尸进程，但是也并不代表僵尸进程不会存在。并且父进程退出时，
# 应该让子进程一起退出，保证不出现孤儿进程。清理进程、关闭子进程等其本质无非就是通知或者向操作系统发出信号，
# 可以通过os模块的一些方法、属性和signal模块的信号完成
# -> https://www.cnblogs.com/Tour/p/5180801.html
# -> https://cloud.tencent.com/developer/news/299111
# -> https://blog.csdn.net/songhaixing2/article/details/113064627
# -> https://blog.csdn.net/whatday/article/details/104375996
# -> https://segmentfault.com/q/1010000012103139?_ea=2875343
