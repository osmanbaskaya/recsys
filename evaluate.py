
from __future__ import division
import dataload
from random import shuffle
from utility import mae, sim_cosine
import numpy as np
from regres import KNeighborRegressor
from evalmetrics import PrecisionRecall

class Evaluater(object):

    def __init__(self, datafile, eval_metric=mae,
                        k=5, sim_method=sim_cosine, test_percentage=30):

        self.datafile = datafile
        self.per = test_percentage / 100
        self.k = k
        self.sim_method = sim_method
        self.eval_metric = eval_metric

        # These will be initiated later.
        self.dataset = None
        self.n_inst = None
        self.trainset = None
        self.testset = None
        self.rec = None
        #FIXME
        self.prepareEvaluater()

    def prepareEvaluater(self):
        self.dataset = dataload.get_dataset(self.datafile)
        if self.dataset:
            self.__prepare_datasets()
        self.createRecSystem()

    def createRecSystem(self):
        
        db, idb, movies = dataload.read_data_to_hash(self.trainset)
        self.rec = KNeighborRegressor(db, idb, k=self.k, 
                                        sim_method=self.sim_method)
        


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
        #TODO: self.eval_metric?
        return mae(rating_array[:,0], rating_array[:,1])

    def __calc_pr(self, test_db, k=1, N=20, I=1000):
        #TODO args, kwargs
        pr = PrecisionRecall(self.dataset, test_db, N, I)
        pression_recall = []
        for user in test_db.iterkeys():
            

            
            precision, recall = pr.evaulate_pr()

        return precision, recall
        


    def evaluate(self, k=1, N=20, I=1000):

        """
            Input:
                -> k: Number of item(s) which are/is the user appreciates
                   most.
        """

        test_db = dataload.read_data_to_hash(self.testset)[0]


        if self.eval_metric.func_name == mae.func_name: 
            return self.__calc_mae(test_db)
        elif self.eval_metric == 'pr': # precision & Recall
            print 'pr'
            return self.__calc.pr(test_db, k, N, I)
        else:
            print "BURADA"
            



