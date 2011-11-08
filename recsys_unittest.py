#! /usr/bin/python
# -*- coding: utf-8 -*-


import unittest

from utility import *
import numpy as np
from math import sqrt



class similartyTest(unittest.TestCase):

    def setUp(self):
        self.t = np.array([1,2,3,4])
        self.t1 = np.array([0, 0, 0, 0])
        self.t2 = np.array([4,3,2,1])
        self.h1 = [1,0,0,1,1]
        self.h2 = [1,1,1,1,1]

    def test_euclidean(self):
        self.failUnless(euclidean(self.t, self.t) == 0)
        self.failUnless(euclidean(self.t, self.t1) == sqrt(30))
    
    def test_pearson(self):
        self.failUnless(sim_pearson(self.t, self.t) == 1)
        self.failUnless(sim_pearson(self.t, self.t2) == -1)
        #TODO :  tam deger ekle

    def test_cosine(self):
        self.failUnless(sim_cosine(self.t, self.t) == 0)
        self.failIf(sim_pearson(self.t, self.t1) == -1)
        #TODO :  tam deger ekle

    def test_hamming(self):
        self.failUnless(hamming(self.h1, self.h1) == 0)
        self.failUnless(hamming(self.h1, self.h2) == 2)
        self.failUnless(hamming(self.t1, self.t2) == 4)
        self.failUnless(hamming(self.t1, self.t1) == 0)

    def test_normalize(self):
        t_n = normalize(self.t)
        self.failUnless(t_n.sum() == 0)
        self.failUnless(t_n.std() == 1)


    def test_parallel_distance(self):
        p = get_parallel_dict()
        k = sim_cosine(self.t, self.t, signature=1)
        self.failUnless(p[1] == k)
        k = euclidean(self.t, self.t1, signature=2)
        self.failUnless(p[2] == k)


class evaluationTest(unittest.TestCase):
    
    def setUp(self):
        self.t = np.array([1,2,3,4])
        self.t1 = np.array([0, 0, 0, 0])
        self.h1 = [1,0,0,1]

    def test_mae(self):
        self.failUnless(mae(self.t, self.t1) == 2.5)
        self.failUnless(mae(self.h1, self.t1) == mae(self.t1, self.h1) == 0.5)

    def test_rmse(self):
        self.failUnless(False)

    def test_precision(self):
        self.failUnless(False)
    
    def test_recall(self):
        self.failUnless(False)


def main():
    unittest.main()
    


if __name__ == '__main__':
    main()
        
        
