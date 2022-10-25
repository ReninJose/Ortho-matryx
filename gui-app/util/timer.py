from functools import wraps
from time import time


ColorCodes = {
    'reset' : '\033[0m',
    'red'   : '\033[31m',
    'green' : '\033[32m',
    'orange': '\033[33m',
    'blue'  : '\033[34m',
    'purple': '\033[35m',
    'cyan'  : '\033[36m'
}


def timed(code=ColorCodes['reset']):
    def wrapper(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            color = ColorCodes[code]
            reset = ColorCodes['reset']
            print(f'{color}Start: {func.__name__!r} with args {args} {kwargs} {reset}')
            start = time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time()
                total = end - start
                print(f'{color}Finish: {func.__name__!r} in {total:.4f} second(s)')

        return wrapped
    return wrapper


