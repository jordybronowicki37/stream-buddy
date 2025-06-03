from time import sleep, time
from typing import Callable


def extend_function_runtime(sec: int, func: Callable[[], None]):
    start_time = time()
    func()
    elapsed = time() - start_time
    time_to_sleep = max(sec - elapsed, 0)
    sleep(time_to_sleep)
