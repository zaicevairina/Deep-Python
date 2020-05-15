import cProfile
import pstats
import logging

logging.basicConfig(filename='logs.log', level=logging.DEBUG)


def profile(func):
    """Decorator for run function profile"""

    def wrapper(*args, **kwargs):
        profile_filename = func.__name__ + '.txt'
        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)
        profiler.dump_stats(profile_filename)
        return result

    return wrapper


@profile
def func(list_of_numbers):
    logging.info('begin function')
    arr = []
    if isinstance(list_of_numbers, list):
        N = len(list_of_numbers)
        if N > 1:
            logging.debug('len of list great 1')
            for i in range(N):
                k = 1
                for j in range(N):
                    if i != j:
                        k *= list_of_numbers[j]
                arr.append(k)
            logging.debug('return result')
            return arr
        else:
            logging.error('len of list less 1')
            raise ValueError
    else:
        logging.critical('type not list')
        raise TypeError


if __name__ == '__main__':
    func(list(range(1, 1001)))

    p = pstats.Stats("func.txt")
    print(p.strip_dirs().sort_stats("time").print_stats())
