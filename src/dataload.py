#! /usr/bin/python
# -*- coding: utf-8 -*-


__author__ = "Osman Baskaya"
__date__ = "Wed Sep 21 16:15:37 EEST 2011"

"""Collabrative filtering on MovieLens 100K data*.

*: http://www.grouplens.org/system/files/ml-100k.zip

"""

from pickle import dump, load
from sys import stderr

PATH = '../dataset/'


def read_data_to_hash(dataset='u.data', path=PATH, reverse_key=True,
                        item_based=False):
    try:
        f = open(path+dataset, 'r')
        data = f.readlines()
    except IOError: # No such file exists. In that case
        data = dataset
    except TypeError:
        data = dataset
    else: # If Try clause doesn't raise any exception..
        f.close()
    user_hash = dict()
    item_hash = dict()
    for line in data: 
        #user, item, rating, ts = line.split('\t')
        user, item, rating, ts = line.split('::')
        #TODO: Clean these mess
        item = int(item)
        user = int(user)
        user_hash.setdefault(user, {})
        user_hash[user][item] = float(rating)
        if reverse_key:
            item_hash.setdefault(item, {})
            item_hash[item][user] = float(rating)
    movies = None
    if item_based:
        movies = dict()
        for line in open(path+'u.item', 'r'):
            movie_id, title = line.split('|')[0:2]
            movies[int(movie_id)] = title

    return user_hash, item_hash, movies

def get_dataset(datafile):

    try:
        f = open(PATH + datafile, 'r')
    except IOError as e:
        stderr.write("IOError for filename %s : %s\n" % (filename, e.strerror))
        print "Dataset has not been read yet. Please give another datafile"
        exit(1)
        #return None
    return  f.readlines()


def make_serial(obj, filename):

    """ Make serialization of the given object on given filename. """

    try:
        f = open(filename, 'w')
    except IOError as e:
        stderr.write("IOError for filename %s : %s\n" % (filename, e.strerror))
    else:
        dump(obj, f)
        f.close()


def load_sll_data(filename):

    """Load and return the serialization object according to filename"""

    try:
        f = open(filename)
    except IOError as e:
        stderr.write("IOError for filename %s : %s\n" % (filename, e.strerror))
    else:
        return load(f)

def main():
    #TODO: raise Error
    pass
    

if __name__ == '__main__':
    main()
