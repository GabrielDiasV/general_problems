import unittest 
import time
from fibonacci import cache_fib_n
from types import FunctionType

TIMEOUT = 10


def measure_time(func: FunctionType, *args, **kwargs):
    start_time = time.time()
    output = None
    if callable(func):
        output = func(*args, **kwargs)
    elapsed_time = time.time() - start_time
    return elapsed_time


def calc_fibonacci(start_time: float, timeout: float, fib_numb: int, output_container: dict):
    delay = time.time() - start_time

    if delay > timeout:
        raise TimeoutError
    
    output_container.update({0:0, 1:1})
    if fib_numb not in output_container.keys():
        output_container[fib_numb] = calc_fibonacci(start_time, timeout, fib_numb-1, output_container)+ calc_fibonacci(start_time, timeout, fib_numb-2, output_container)
    
    return output_container[fib_numb] 



class TestFibonnaci(unittest.TestCase):

    def test_value_correct(self):
        self.assertEqual(calc_fibonacci(time.time(), TIMEOUT, 10, {}), cache_fib_n(10))
        self.assertEqual(calc_fibonacci(time.time(), TIMEOUT, 8, {}), cache_fib_n(8))
        self.assertEqual(calc_fibonacci(time.time(), TIMEOUT, 12, {}), cache_fib_n(12))


    def test_timeout(self):
        with self.assertRaises(RecursionError):
            calc_fibonacci(time.time(), TIMEOUT, 1000, {})


    def test_complexity(self):
        self.assertTrue(measure_time(calc_fibonacci, time.time(), TIMEOUT, 6, {}) <= measure_time(measure_time(cache_fib_n, 6)))
        self.assertTrue(measure_time(calc_fibonacci, time.time(), TIMEOUT, 10, {}) <= measure_time(measure_time(cache_fib_n, 10)))
        self.assertTrue(measure_time(calc_fibonacci, time.time(), TIMEOUT, 16, {}) <= measure_time(measure_time(cache_fib_n, 16)))


if __name__ == "__main__":
    unittest.main()
