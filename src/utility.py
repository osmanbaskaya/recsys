#! /usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import scipy.linalg as linalg
from math import acos
import numpy as np
from scipy.stats.stats import ss
from functools import wraps



dynamic_programming = True

if dynamic_programming:
    p_dist = dict()

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

def recall(a, b):
    pass

def precision(a, b):
    pass
    

def dynamic_prog(hashtable):
    def wrapper(func):
        if dynamic_programming:
            @wraps(func)
            def dynamic_p(*args, **kwargs):
                sign = kwargs.get('signature')
                if sign is not None:
                    if sign in hashtable:
                        r = hashtable[sign] # hit.
                        return r
                r = func(*args, **kwargs)
                hashtable[sign] = r # register for future hits.
                return r
            return dynamic_p
        else:
            return func
    return wrapper

# Similarity Metrics

#@dynamic_prog(p_dist)
#def sim_adjcosine(a, b, signature=None): 
    #"""
    #This is the cosine similarity explaning with "Adjusted Cosine Similarity"
    #on RSH, p. 125
    
    #input:
    #output:
        #-> degree: a float value. 0<= degree <= pi
    #"""
    #val = a.dot(b) / (linalg.norm(a)*linalg.norm(b))
    #val = max(min(1, val), 0) # avoiding to domain error.
    #degree = acos(val)
    #return degree

@dynamic_prog(p_dist)
def sim_cosine(a, b, signature=None):

    """
    This is the cosine similarity. There is no distinct function such as
    Adjusted Cosine or Cosine Similarity. Because they do same job.
    Only one difference is vectors which are given. The former takes only
    common elements which explained on RSH, p.125; latter one explaned on
    RSH, p.124 takes all elements which is rated by at least one of the user.
    
    input:
    output:
        -> degree: a float value. Intervals: 0<= degree <= pi
    """
    val = a.dot(b) / (linalg.norm(a)*linalg.norm(b))
    val = max(min(1, val), 0) # avoiding to domain error.
    degree = acos(val)
    return degree



@dynamic_prog(p_dist)
def sim_pearson(a, b, signature=None):

    mean_a = a.mean()
    mean_b = b.mean()
    am, bm = a-mean_a, b-mean_b
    r_num = np.add.reduce(am*bm)
    r_den = np.sqrt(ss(am)*ss(bm))
    r = (r_num / r_den)
    return max(min(r, 1.0), -1.0)


@dynamic_prog(p_dist)
def euclidean(a, b, signature=None):
    
    val = np.sqrt(np.add.reduce((a - b)**2))
    return val

@dynamic_prog(p_dist)
def hamming(a, b, signature=None):
    
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


def get_p_dist():
    return p_dist

#def get_p_predict():
    #return p_predict



