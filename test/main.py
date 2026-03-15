def wrapper(func):
    print("before running the function")
    print(f"function name : {func.__name__}")
    return func()


swf