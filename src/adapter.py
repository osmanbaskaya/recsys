#! /usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np


class MovieLensAdapter(object):
    """
        An adapter for MovieLens Data.
        MovieLens dataset is a different than usual UCI Machine Learning dataset.
        Thus, we should use an adapter to handle different type of formats.

    """


    def __init__(self, db, idb = None):
        """
            Input:
                db => user db (e.g: {1:{393:5, 323:3, ... }, ...} )
                idb => item db (e.g: {393:{1:5, 3:2, ...}, ... } )
        """
        self.db = db
        self.idb = idb

    def get_common_elements(self, e1, e2):
        # The switching from numpy to list gains 10 sec for exc. time

        common_items = []
        for item, rating in self.db[e1].iteritems():
            if item in self.db[e2]:
                rating2 = self.db[e2][item]
                common_items.append([item, rating, rating2])
        return common_items

    def sim_prep(self, e1, e2, sim_method):
        common = self.get_common_elements(e1, e2)
        
        #r1_A = r2_A = np.array([]) #So bad.
        r1_A = []; r2_A = []

        if common:
            if sim_method == 'sim_cosine1':
                pass
            elif sim_method in ('euclidean', 'sim_cosine',):
                #common_A = np.array(common)
                #r1_A, r2_A = common_A[:,1], common_A[:,2]
                for k, i, j in common:
                    r1_A.append(i)
                    r2_A.append(j)
            elif sim_method in ('hamming',):
                #FIXME:
                common_A = np.array(common)
                r1_A, r2_A = common_A[:,1], common_A[:,2]
                r1_A, r2_A = r1_A.tolist(), r2_A.tolist() 
        
        return r1_A, r2_A


