import time
from colorama import Fore, Back, Style, init

init(autoreset=True)

# ====== Decorators =================================================================


def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"{Fore.YELLOW}[F] FUCTION: {func.__name__}()")
        result = func(*args, **kwargs)
        print(
            f"{Fore.GREEN}{Style.DIM}[✔️] Completed: {func.__name__}() - Time taken: {time.time() - start_time:.2f} seconds"
        )
        return result

    return wrapper
