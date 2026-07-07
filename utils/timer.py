"""
Module tien ich do thoi gian chay cua 1 ham (dung de benchmark thuat toan).
"""

import time


def measure_time(func, *args, **kwargs):
    """
    Do thoi gian thuc thi cua 1 ham bat ky.

    Tham so:
        func: ham can do thoi gian
        *args, **kwargs: cac tham so truyen vao ham do

    Tra ve:
        (ket_qua_cua_ham, thoi_gian_chay_giay)
    """
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    elapsed = end - start
    return result, elapsed
