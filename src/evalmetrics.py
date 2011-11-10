#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import dataload
import numpy as np


__author__ = "Osman Baskaya"




class PrecisionRecall(object): #BaseMetrics.
    
    """ This method evaulates that how much our recommendation's are
    accurate.

    This distincition is very important. 'Precision & Recall' are able
    to characterize the accuracy of recommendation. In contrast, MAE
    provides an idea of the accuracy of prediction.

    The state of art evaluation metric is 'Precision & Recall' for 
    RCs.

    Algorithm:
        -> Get an item called 'i' which the user gave it high rating.
        -> Get large number of items called I that none of them are 
        relevant for the user.
        -> Predict for every item in set(I+i)
        -> Return top-N list.
        -> If i is in top-N list that means a hit, 
           else a miss.
    """

    def __init__(self, dataset, test, N=20, I=300):
        
        """ Input: 
            -> dataset <list> : all data in list form.
            -> N <Integer> : Length of the recommendation list.
            -> I <Integer> : Number of Pseudo-items. The assumption is that
               all of these items are not relevant for our user[1].
            -> test  <<user => {movie => rating}>,
                     <movie => {user => rating}>>: Contains test dbs. 


        [1]: Cremonesi, P., Milano, P. & Turrin, R., 2010. Performance of
        Recommender Algorithms on Top-N Recommendation Tasks. Methodology, 
        p.39. Available at: http://portal.acm.org/citation.cfm?id=
        1864708.1864721
        
        """

        self.test_db, self.test_idb = test
        self.N = N
        self.db, self.idb, movies = dataload.read_data_to_hash(dataset)
        self.I = I
        
        self.n_hit = 0
        self.n_miss = 0
        self.recall = 0
        self.precision = 0

        print self





    def get_unrelevant_items(self, u):
        """ Returns unrelevant [unrated] items for user u 
            
            SORU : Tum set mi kullanilmali yoksa training set mi?
        """
        user_item = set(self.idb[u].keys())
        all_items = set(self.db.keys())
        diff_items = list(all_items.difference(user_item))
        return diff_items[:self.I] # return I many of items.



    def create_topN_list(self, rating_list):
        rating_array = np.array(rating_list)
        I = np.argsort(rating_array[:,1])
        topNList = rating_array[I, :]
        return topNList[-self.N:] # negative. This is asc. We need high values


    
    def evaluate_precision(self):
        self.precision = self.recall / self.N


    def evaulate_recall(self):
        self.recall = self.n_hit / (self.n_hit + self.n_miss)


    def get_important_items_from_testset(self):
        """
            Returns user-item generator in which items are rated high by the user.

        """
        #FIXME : Is there more efficient way? Ask StackOverFlow
        userItem = ((u, i.keys()[0]) for u, i in  self.test_db.iteritems() 
                    if i.values()[0] == 5 ) # userItem is 5 rated film
        return userItem


    def evaluate_pr(self):
        self.evaulate_recall()
        self.evaluate_precision()
        return self.precision, self.recall
        
    def use_for_pr(self, topNList, item):
        print "#########topNList###########\n", topNList
        if item in topNList:
            self.n_hit += 1
            print 'hit for item:%s\n' % item
        else:
            self.n_miss += 1
            print 'miss for item:%s\n' % item


    def __str__(self):
        metric_name = "Precision & Recall"
        N = self.N
        I = self.I
        l_test = len(self.test_idb)
        return 'Evaluater Metric:%s\nN:%s\n#of Unrelevant Items:%s\nLength of the test Set:%s\n' % (metric_name, N, I, l_test)


    #def get_important_items(self, u, k):
        #""" Returns k many of item(s) that are rated high scores by user u """
        
        #items = np.array(self.db[u].items()) # array of [item_id, rating]
        #I = np.argsort(items[:, 1]) # sort by rating
        #imp_items = items[I, :][-k:] # last k items which are probably rated by 5
        #return imp_items[:, 0] # return only item_id(s) of important items
