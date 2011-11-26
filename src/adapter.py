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
        
        self.numberOfKeyError = 0 #TODO: Islem Bittikten sonra bu deger 
                                  # sifira dondurulmesi gerekmekte


    def get_union(self, e1, e2):



        i_e1 = self.db[e1]
        i_e2 = self.db[e2]

        items = []
        union_items = []

        for item, rating in i_e1.iteritems():
            if item in i_e2:
                rating2 =  i_e2[item]
            else:
                rating2 = 0

            union_items.append([item, rating, rating2])
            items.append(item)
        
        for item, rating2 in i_e2.iteritems():
            if item not in items:
                if item in i_e1:
                    rating = i_e1[item]
                else:
                    rating = 0
                union_items.append([item, rating, rating2])
                items.append(item)
        return union_items



       

    def get_common_elements(self, e1, e2):
        
        common_items = []
        
        try: 
            for item, rating in self.db[e1].iteritems():
                if item in self.db[e2]:
                    rating2 = self.db[e2][item]
                    common_items.append([item, rating, rating2])
        except KeyError:
            self.numberOfKeyError += 1 
            return None

        return common_items

    def sim_prep(self, e1, e2, sim_method):
        r1_A = r2_A = np.array([])

        if sim_method == 'sim_cosine':
            union = self.get_union(e1, e2)
            union_A = np.array(union)
            r1_A, r2_A = union_A[:,1], union_A[:,2]
        else:
            common = self.get_common_elements(e1, e2)
            if common:
                if sim_method in ('euclidean', 'sim_adjcosine',):
                    common_A = np.array(common)
                    r1_A, r2_A = common_A[:,1], common_A[:,2]
                elif sim_method in ('hamming',):
                    #FIXME:
                    common_A = np.array(common)
                    r1_A, r2_A = common_A[:,1], common_A[:,2]
                    r1_A, r2_A = r1_A.tolist(), r2_A.tolist() 
        
        return r1_A, r2_A


