#! /usr/bin/python
# -*- coding: utf-8 -*-

from evaluate import Evaluater
from itertools import product
import cProfile


def main():
    f = open('test_results.txt', 'a+')
    k_val = [5]
    per = [30]
    #k_val = [3, 9, 13, 17, 21]
    iterate = product(per, k_val)
    for per, k in iterate:
        f.write(str([per, k]) + '\t')
        e = Evaluater('u.data', k=k, test_percentage=per)
        f.write(str(e.evaluate()) + '\n')
    f.close()


if __name__ == '__main__':
    #cProfile.run('main()')
    main()
