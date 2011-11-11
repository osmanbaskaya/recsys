#! /usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import division
from utility import sim_cosine, get_p_dist
import numpy as np
from adapter import MovieLensAdapter



class BaseEstimator(object):

    def __init__(self, db, idb=None, movies=None, k=5, sim_method=sim_cosine,
                        r_method='uniform'):
        self.k = k
        self.movies = movies
        self.sim_method = sim_method
        self.db = db  # a dictionary for all items.
        self.idb = idb
        self.r_method = r_method
        self.adapt = MovieLensAdapter(self.db, self.idb) # adapter
        self.parallel = get_p_dist()


    def find_neighbors(self, e, item):

        if self.idb:
            try:
                potential_users = dict(self.idb[item])
            # There is no potential user in training data who watch this movie
            except KeyError: 
                return None # It will be handled by "find_distances" method
            if e in potential_users.keys():
                potential_users.pop(e)
            return potential_users
        else: 
            #TODO: If we haven`t any different idb dictionary..
            pass

    def find_distances(self, e, potential_users):

        #mov_e = self.adapt.convertMovie2array(e)
        n_list = []
        for p_user, rating in potential_users.iteritems():
            key = str(set([e, p_user]))
            #if key in self.parallel:
                #print "parallelized"
                #return self.parallel[key]
            e_A, p_user_A = self.adapt.sim_prep(e, p_user,
                                              self.sim_method.func_name)
            # If there is no item in common, no need to evaluate the distance
            #if e_A.any():
                #dist = self.sim_method(e_A, p_user_A, signature=key)
                #n_list.append([p_user, dist, rating])
            #if e_A is not None:
                #dist = self.sim_method(e_A, p_user_A, signature=key)
                #n_list.append([p_user, dist, rating])
            try:
                dist = self.sim_method(e_A, p_user_A, signature=key)
                n_list.append([p_user, dist, rating])
            except:
                pass
        n_list = np.array(n_list)
        I = np.argsort(n_list[:, 1])  # sorting by distance
        n_neighbors = n_list[I, :]
        try:
            k = n_neighbors[:self.k, :]
        except IndexError:
            print 'IndexError'
            exit()
        return k


