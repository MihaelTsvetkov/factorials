import timeit
import sys
import multiprocessing

sys.set_int_max_str_digits(2000000000) # Увеличиваем максимальное кол-во цифр для вывода


# Первый самый банальный способ

def classic_method_to_calculate_factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return f'factorial {n}! = {result}\n'


# Второй способ интереснее, мы находим все простые множители для каждого числа от 1 до n и считаем их общее
# количество, затем возводим их в степень их количества и перемножаем результат

# Функция для нахождения простых множителей
def prime_factors(n):
    i = 2
    factors = {}
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            if i in factors:
                factors[i] += 1
            else:
                factors[i] = 1
    if n > 1:
        if n in factors:
            factors[n] += 1
        else:
            factors[n] = 1
    return factors


# Функция, которая возводит все простые множители в степень и перемножает их, а затем выводит результат
def prime_method(n):
    factor_counts = {}
    for i in range(2, n + 1):
        for prime, count in prime_factors(i).items():
            if prime in factor_counts:
                factor_counts[prime] += count
            else:
                factor_counts[prime] = count

    result = 1
    for prime, count in factor_counts.items():
        result *= prime ** count
    return f'factorial {n}! = {result}\n'


# В третьем способе мы делим последовательность от 1 до n на определенное число (зависит от мощности процессора),
# получаем определенное количество последовательностей (например: (1, 10), (11, 20), (21, 30) и т.д.) Затем в отдельных
# процессах мы перемножаем все элементы последовательностей между собой (одной последовательности один процесс)
# После этого перемножаем результаты между собой

def chunk_range(start, end, chunk_size):
    for i in range(start, end, chunk_size):
        yield (i, min(i + chunk_size, end))


def factorial_range(start, end):
    result = 1
    for i in range(start, end + 1):
        result *= i
    return result


def parallel_method(n, num_processes):
    if num_processes > n:
        num_processes = n
        print(f'Слишком большое число процессов для числа {n}, число процессов '
              f'автоматические изменено на {num_processes}')

    chunk_size = n // num_processes
    ranges = list(chunk_range(1, n + 1, chunk_size))

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(factorial_range, ranges)

    final_result = 1
    for res in results:
        final_result *= res

    return f'factorial {n}! = {final_result}\n'


if __name__ == "__main__":
    number = 100000
    num_processes = 4

    setup_code = '''
from __main__ import parallel_method
'''
    execution_code = f'''
parallel_method({number}, {num_processes})
'''

    # Каждый тест запускается по 5 раз и выводится лучший результат

    execution_time = timeit.repeat(stmt=execution_code, setup=setup_code, repeat=5, number=1)
    print("Parallel method:", min(execution_time))

    classic_method_time = timeit.repeat("classic_method_to_calculate_factorial(number)", globals=globals(),
                                        repeat=5, number=1)
    print("Classic method time:", min(classic_method_time))

    prime_method_time = timeit.repeat("prime_method(number)", globals=globals(), repeat=5, number=1)
    print("Prime method time:", min(prime_method_time), "\n")


