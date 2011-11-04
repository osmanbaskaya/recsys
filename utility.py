#! /usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import scipy.linalg as linalg
from math import acos
import numpy as np
from scipy.stats.stats import ss


# Evaluation Metrics

def mae(a, b):
    
    n = len(a)
    try:
        error = np.abs(a - b).sum() / n 
    except TypeError: # a or b is not ArrayType
        a = np.array(a)
        b = np.array(b)
        error = np.abs(a - b).sum() / n

    return error

# Similarity Metrics

def sim_cosine(a, b):
    """
    input:
    output:
        -> degree: a float value. 0<= degree <= pi
    """
    val = a.dot(b) / (linalg.norm(a)*linalg.norm(b))
    val = max(min(1, val), 0) # avoiding to domain error.
    degree = acos(val)
    return degree

def sim_pearson(a, b):

    mean_a = a.mean()
    mean_b = b.mean()
    am, bm = a-mean_a, b-mean_b
    r_num = np.add.reduce(am*bm)
    r_den = np.sqrt(ss(am)*ss(bm))
    r = (r_num / r_den)
    return max(min(r, 1.0), -1.0)


def euclidean(a, b):
    
    val = np.sqrt(np.add.reduce((a - b)**2))
    return val

def hamming(a, b):
    
    n = len(a)
    counter = 0
    #diff = n - len(np.intersect1d(a,b))
    for i in xrange(n):
        if a[i] != b[i]:
            counter += 1
    return counter


def normalize(X):
    X_m = X - X.mean(axis=0)
    X_n = X_m / X.std(axis=0)
    return X_n
