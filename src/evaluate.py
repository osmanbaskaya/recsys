
from __future__ import division
import dataload
from random import shuffle
from utility import mae, sim_cosine
import numpy as np
from regres import KNeighborRegressor
from evalmetrics import PrecisionRecall
from sys import stderr

class Evaluater(object):

    def __init__(self, datafile, rec_type='ub', eval_metric='mae',
                        k=5, sim_method=sim_cosine, test_percentage=30):

        self.datafile = datafile
        self.per = test_percentage / 100
        self.k = k
        self.sim_method = sim_method
        self.eval_metric = eval_metric
        self.rec_type = rec_type

        # These will be initiated later.
        self.dataset = None
        self.n_inst = None
        self.trainset = None
        self.testset = None
        self.rec = None
        #FIXME
        self.prepareEvaluater()
        print self
        print '\n'

    def prepareEvaluater(self):
        self.dataset = dataload.get_dataset(self.datafile)
        
        #if self.rec_type == 'ub': # userbased
            #self.dataset = dataload.get_dataset(self.datafile)
        #elif self.rec_type == 'ib': # itembased
            #pass
        #else:
            #stderr.write("Please enter ub [user-based] or ib [item-based]")
            #exit(1)
        #if self.dataset:
        self.__prepare_datasets()
        self.createRecSystem()

    def createRecSystem(self):
        
        db, idb, movies = dataload.read_data_to_hash(self.trainset)

        self.rec = KNeighborRegressor(db, idb, k=self.k, 
                    sim_method=self.sim_method, rec_type=self.rec_type)
        


    def __prepare_datasets(self):
        #TODO this method may be in dataload module.

        self.n_inst = len(self.dataset)
        shuffle(self.dataset)
        n_test_inst = int(self.per * self.n_inst)
        self.testset = self.dataset[:n_test_inst]
        self.trainset = self.dataset[n_test_inst:]
        total = sum(map(len, [self.trainset, self.testset])) 
        assert total == self.n_inst


    def __calc_mae(self, test_db):
        """ This method evaluates that how much our prediction's 
        are accurate.
        
        This distinction is very important. MAE is able to characterize the 
        accuracy of prediction not accuracy of recommendation[1].
        
        If you want to evaluate accuracy of prediction, you should 
        use 'pr' rather than 'mae'. 'pr' provides you Precision and Recall.
        
        [1]: Symeonidis, P. et al., 2006. Collaborative Filtering: Fallacies
        and Insights in Measuring Similarity. In citeulikeorg. Citeseer, 
        p. 56. Available at: 
        http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.61.8340&
        rep=rep1&type=pdf.

        """
        rating_list = []
        for user, itemRating in test_db.iteritems():
            # user : integer - user_id
            # itemRating : dictionary - { item_id:Rating, ... }
            rating = self.rec.predict(user, itemRating.keys()[0])
            rating_list.append([rating, itemRating.values()[0]])

        rating_array = np.array(rating_list)
        print "Number of key error: %s" % self.rec.adapt.numberOfKeyError
        #TODO: self.eval_metric?
        return mae(rating_array[:,0], rating_array[:,1])



    def __calc_pr(self, test_db, k=1, N=20, I=300):
        #TODO args, kwargs
        #pr = PrecisionRecall(self.dataset, test_db, N, I)
        pr = PrecisionRecall(self.trainset, test_db, N, I)
        rating_list = []
        actual_testset = pr.get_important_items_from_testset() # This item is high rated by users.
        #print 'Actual Length of the Testset%s\n' % actual_testset
        for user, item in actual_testset:
            #print "\nNew test for user_id=%s, item_id=%s\n" % (user, item)
            unrev_items = pr.get_unrelevant_items(user)
            
            if unrev_items is not None:

                unrev_items.append(item) # added our relevant item for prediction
                assert len(unrev_items) == I + 1
                for item in unrev_items:
                    key = str(user) + '_' + str(item)
                    rating = self.rec.predict(user, item, signature=key)
                    rating_list.append([item, rating])
                topNList = pr.create_topN_list(rating_list)
                pr.use_for_pr(topNList, item) # use this inf. for calculating PR

        precision, recall = pr.evaluate_pr()
        return precision, recall
        


    def evaluate(self, k=1, N=20, I=300):

        """
            Input:
                -> k: Number of item(s) which are/is the user appreciates
                   most. (Only for Precision & Recall)
        """
        test_db, test_idb, m = dataload.read_data_to_hash(self.testset)
        if self.rec_type == 'ib':
            test_db, test_idb = test_idb, test_db
        if self.eval_metric == 'mae':
            return self.__calc_mae(test_db)
        elif self.eval_metric == 'pr': # precision & Recall
            return self.__calc_pr((test_db, test_idb), k, N, I)
        else:
            stderr.write("There is no such evaluation metric you can use")
            exit(1) 

    def __str__(self):
        p = self.per
        d_f = self.datafile
        k = self.k
        sim = self.sim_method.func_name
        return 'Evaluater\nDatafile:%s\ntest_percentage:%s\nk:%s\nSimilarity Method:%s' % (d_f,p,k,sim)


