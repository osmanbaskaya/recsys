
from __future__ import division
import dataload
from random import shuffle
from utility import mae, sim_cosine
import cProfile
from itertools import product
import numpy as np
from regres import KNeighborRegressor

class Evaluater(object):

    def __init__(self, datafile, k=5, sim_method=sim_cosine, test_percentage=30):

        self.datafile = datafile
        self.per = test_percentage / 100
        self.k = k
        self.sim_method = sim_method

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
        self.rec = KNeighborRegressor(db, idb, k=self.k, sim_method=self.sim_method)
        


    def __prepare_datasets(self):

        self.n_inst = len(self.dataset)
        shuffle(self.dataset)
        n_test_inst = int(self.per * self.n_inst)
        self.testset = self.dataset[:n_test_inst]
        self.trainset = self.dataset[n_test_inst:]
        total = sum(map(len, [self.trainset, self.testset])) 
        assert total == self.n_inst

    def evaluate(self):
        test_db = dataload.read_data_to_hash(self.testset)[0]
        rating_list = []
        for user, itemRating in test_db.iteritems():
            # user : integer - user_id
            # itemRating : dictionary - { item_id:Rating, ... }
            rating = self.rec.predict(user, itemRating.keys()[0])
            rating_list.append([rating, itemRating.values()[0]])

        rating_array = np.array(rating_list)
        return mae(rating_array[:,0], rating_array[:,1])


def main():
    f = open('test_results', 'a+')
    #per = [10, 20, 30]
    k_val = [27,33,37,41,45,51]
    per = [30]
    #k_val = [5]
    iterate = product(per, k_val)
    for per, k in iterate:
        f.write(str([per, k]) + '\t')
        e = Evaluater('u.data', k=k, test_percentage=per)
        f.write(str(e.evaluate()) + '\n')
    f.close()



if __name__ == '__main__':
    cProfile.run('main()')
    #main()
