#! /usr/bin/python
# -*- coding: utf-8 -*-


from dataload import read_data_to_hash
from regres import KNeighborRegressor
from utility import euclidean, sim_pearson

db, idb, movies  = read_data_to_hash()
r = KNeighborRegressor(db, idb, movies, k=5)
print r
print r.predict(1, 2)

#def main():
    #pass


#if __name__ == '__main__':
    #main()
