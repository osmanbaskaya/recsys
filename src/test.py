#! /usr/bin/python
# -*- coding: utf-8 -*-

from evaluate import Evaluater
from itertools import product
import cProfile
from time import gmtime, strftime


item_based = True

def main():
    f = open('../testres.txt', 'a+')
    k_val = [10]
    per = [30]
    #per = [1.4]

    #per = [1.4]
    #k_val = [3, 9, 13, 17, 21]
    test_name = "New User-based Test on: "
    if item_based:
        test_name  = "New Item-based test on: "
    iterate = product(per, k_val)
    for per, k in iterate:
        f.write('\n')
        timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        f.write(test_name + timestamp + ' --> ')
        e = Evaluater('u.data', rec_type='ub', k=k, test_percentage=per, 
                                                eval_metric='mae')
        f.write(str([per, k, e.eval_metric, e.sim_method.func_name]) + ' Error: ')
        f.write(str(e.evaluate()))
    f.close()


if __name__ == '__main__':
    #cProfile.run('main()')
    main()
