import pytest,time
def func_exit():
    try:
        raise SystemExit(1)
    except SystemExit as e:
        print("caught in func_exit:", e.code)
        raise # 重新抛出异常，让外层可以捕获
    else:
        print("not caught in func_exit")
    finally:
        print("finally in func_exit")
def test_func_exit():
    with pytest.raises(SystemExit) as excinfo:
        func_exit() 
    print("caught in test_func_exit:", excinfo.value.code)

#装饰器和闭包
# 闭包是指在一个函数内部定义了另一个函数，并且内部函数引用了外部函数的变量。即使外部函数已经执行完毕，这些变量仍然会保存在内存中。闭包的形成条件包括：
# 在一个外部函数中定义了一个内部函数。
# 内部函数使用了外部函数的变量或参数。
# 外部函数返回了内部函数的引用
num1 = 10 # 全局变量
def outer():
    num2 = 20 # 外部函数的局部变量
    def inner():
        global num1
        num3 = 30 # 内部函数的局部变量
        return num1 + num2 + num3
    return inner
# 其中，num1是全局变量，在inner方法内使用时需要使用global进行声明；num3是局部变量，在inner方法内定义并使用
# 但是对inner来说，num2自由变量
def showtime(func):
    def wrapper():
        start_time = time.time()
        func()
        end_time = time.time()
        print('spend is {}'.format(end_time - start_time))
    return wrapper

@showtime
def foo():
    print('foo..')
    time.sleep(3)
# 装饰器是闭包的一种应用，它用于在不修改原函数代码的情况下，给函数增加新的功能。装饰器的形成条件包括：
# 不修改已有函数的源代码。
# 不修改已有函数的调用方式。
# 给已有函数增加额外的功能。
# @staticmethod、@classmethod 和 @property Python内置的3种函数装饰器
if __name__ == "__main__":
    #test_func_exit()
    test=outer()
    result=test()
    print("闭包结果:",result)
    foo ()