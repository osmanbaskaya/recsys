#! /usr/bin/python
# -*- coding: utf-8 -*-

from evaluate import Evaluater
from itertools import product
import cProfile
from time import gmtime, strftime


item_based = True

def main():
    testbase = 'ub'
    
    dataset_name = "u1m.data"
    f = open('../testres.txt', 'a+')
    
    k_val = [5]
    per = [30]
    #per = [1.4]
    #metric = 'pr'
    metric = 'mae'

    #k_val = [5 9, 13, 17, 21]
    


    test_name = "New User-based Test on: "  + dataset_name + ' '
    if item_based:
        testbase = 'ib'
        test_name  = "New Item-based test on: " + dataset_name + ' '
    iterate = product(per, k_val)
    for per, k in iterate:
        f.write('\n')
        timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        f.write(test_name + timestamp + ' --> ')
        e = Evaluater(dataset_name, rec_type=testbase, k=k, test_percentage=per, 
                                                eval_metric=metric)
        f.write(str([per, k, e.eval_metric, e.sim_method.func_name]) + ' Error: ')
        f.write(str(e.evaluate()))
    f.close()


if __name__ == '__main__':
    #cProfile.run('main()')
    main()
