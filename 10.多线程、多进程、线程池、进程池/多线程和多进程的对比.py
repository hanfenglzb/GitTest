from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
import time


def fib(n):
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)


def sleep(seconds):
    time.sleep(seconds)
    return seconds


if __name__ == '__main__':
    print("多CPU运算操作-线程".center(30, "-"))
    with ThreadPoolExecutor(3) as executor:
        start_time = time.time()
        futures = [executor.submit(fib, n) for n in range(25, 35)]
        for future in as_completed(futures):
            res = future.result()
            print(res)
        end_time = time.time()
        print(end_time - start_time)

    print("多CPU运算操作-进程".center(30, "-"))
    with ProcessPoolExecutor(3) as executor:
        start_time = time.time()
        futures = [executor.submit(fib, n) for n in range(25, 35)]
        for future in as_completed(futures):
            res = future.result()
            print(res)
        end_time = time.time()
        print(end_time - start_time)

    print("多IO操作-线程".center(30, "-"))
    with ThreadPoolExecutor(3) as executor:
        start_time = time.time()
        futures = [executor.submit(sleep, n) for n in [2] * 10]
        for future in as_completed(futures):
            res = future.result()
            print(res)
        end_time = time.time()
        print(end_time - start_time)

    print("多IO操作-进程".center(30, "-"))
    with ProcessPoolExecutor(3) as executor:
        start_time = time.time()
        futures = [executor.submit(sleep, n) for n in [2] * 10]
        for future in as_completed(futures):
            res = future.result()
            print(res)
        end_time = time.time()
        print(end_time - start_time)
