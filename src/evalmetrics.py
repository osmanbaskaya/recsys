#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"


import dataload






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

    def __init__(self, dataset, test_db, N=20, I=1000):
        
        """ Input: 
            -> dataset <list> : all data in list form.
            -> N <Integer> : Length of the recommendation list.
            -> I <Integer> : Number of Pseudo-items. The assumption is that
               all of these items are not relevant for our user[1].
            -> test_db  <user => {movie => rating}>: Contains test data. 


        [1]: Cremonesi, P., Milano, P. & Turrin, R., 2010. Performance of
        Recommender Algorithms on Top-N Recommendation Tasks. Methodology, 
        p.39. Available at: http://portal.acm.org/citation.cfm?id=
        1864708.1864721
        
        """

        self.test_db = test_db
        self.N = N
        self.db, self.idb, movies = dataload.read_data_to_hash(dataset)




    def get_unrelevant_items(self, u):
        pass

    def evaluate_precision(self):
        pass

    def evaulate_recall(self):
        pass

    def get_important_items(self, u, k):
        
        items = self.db[u]
        


    def evaluate_pr(self):
        
        for user, itemRating in self.test_db.iteritems():
            pass

        


