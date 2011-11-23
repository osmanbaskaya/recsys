#! /usr/bin/python
# -*- coding: utf-8 -*-

from evaluate import Evaluater
from itertools import product
import cProfile
from time import gmtime, strftime


def main():
    f = open('../testres.txt', 'a+')
    k_val = [10]
    per = [1.4]

    #per = [1.4]
    #k_val = [3, 9, 13, 17, 21]
    iterate = product(per, k_val)
    for per, k in iterate:
        timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        f.write("New test on: " + timestamp + ' --> ')
        e = Evaluater('u.data', k=k, test_percentage=per, eval_metric='pr')
        f.write(str([per, k, e.eval_metric, e.sim_method.func_name]) + ' Error: ')
        f.write(str(e.evaluate()) + '\n')
    f.close()


if __name__ == '__main__':
    cProfile.run('main()')
    #main()
