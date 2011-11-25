#! /usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from base import BaseEstimator
from utility import dynamic_prog
import numpy as np
from sys import stderr


p_predict = dict() # for parallel programming

class KNeighborRegressor(BaseEstimator):
    
    #def __init__(self, db, idb=None, movies=None, k=5, sim_method=cosine_dist,
                    #r_method='uniform'):

        
        #super(KNeighborRegressor, self).__init__(db, idb, movies, k, \
                                        #sim_method, r_method)
    def __init__(self, *args, **kwargs):
        super(KNeighborRegressor, self).__init__(*args, **kwargs)
        #print self


    def calculate_rating(self, n_list):

        # n_list : [neighor_id, distance, rating]


        if self.r_method == 'uniform':
            arr = n_list
            return arr[:,2].mean()
        elif self.r_method == 'distance':
            w_arr =  (1 / arr[:,1])
            return (w_arr * arr[:,2]).mean() / w_arr.sum()
        else:
            stderr.write("Unrecognized method used to calculate rating\n")
            exit(1)

    @dynamic_prog(p_predict)
    def predict(self, u, item, signature=None):
        
        neighbors = self.find_neighbors(u, item)

        if neighbors is None: # u is not in training db. 
            return 3.5

        if not neighbors:
            # There is no potential user in training data who watch this movie
            mov_e = np.array(self.db[u].values())
            e_mean = mov_e.mean() # return the user`s average rating value
            return e_mean

        n_list = self.find_distances(u, neighbors)
        rating = self.calculate_rating(n_list)
        return rating


    def __str__(self):
        s = "\n### KNeighborRegressor ###\nDetails:\nk : %s,\nsim_method :" + \
        " %s,\nr_method : %s\n"
        
        return s % (self.k, self.sim_method.func_name, self.r_method)
