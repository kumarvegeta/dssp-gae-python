# This Python file uses the following encoding: utf-8

import cgi

#from google.appengine.api import users

import webapp2

#import jinja2

import paste

import webob

import os

#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.feature_extraction.text import TfidfTransformer
#from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds
from scipy.spatial.distance import cosine
from scipy.sparse import csr_matrix

from numpy import (array, dot, arccos, clip)
from numpy.linalg import norm
import json, glob
import re, math, operator
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


from sklearn.preprocessing import normalize

import pickle

from random import randint

def create(file):
    f = open(file,'w')
    f.close()

vocabulary = pickle.load( open( 'vocabulary.pkl', 'rb' ) )
count_vectorizer = pickle.load( open( 'count_vectorizer.pkl', 'rb' ) )
tf_idf_matrix = pickle.load( open( 'tf_idf_matrix.pkl', 'rb' ))

#print(vocabulary)

print len(vocabulary)

#word = ""

#print "Enter a word: "

#word = raw_input()

#word = ""

path = "results_en/"

#print vocabulary.keys()[0].decode('unicode-escape')

word_list = vocabulary.keys() 

for temp in word_list:

    word = temp.decode('unicode-escape')

    if word in vocabulary:
    
        word_index  = vocabulary[word]

        words = vocabulary.keys()

        path += word

        path+= ".txt"

        distance_from_other_words = {}
        vector_1 = csr_matrix(tf_idf_matrix[:,word_index])
        vector_1 = np.array(vector_1.todense())

        N = len(vocabulary) 

    for i in range(N):
        try:
            if word==words[i]:
		pass
	    else:
		vector_2 = tf_idf_matrix[:,i]
		vector_2 = csr_matrix(tf_idf_matrix[:,i])
		vector_2 = np.array(vector_2.todense())
		distance_from_other_words[i] = cosine(vector_1, vector_2)
	except KeyError:
            pass
    sorted_matrix = sorted(distance_from_other_words.items(), key=operator.itemgetter(1), reverse=True)
    results = []
    for item in sorted_matrix:
        w = words[item[0]]
	score = item[1]
        if score !=1.0 and score !=0.0 and score >=0.9:
            results.append([w.encode('utf-8'), score])
    #results = [["Hello_%d"%i, np.random.random()] for i in  range(100)]
            #print "Word:", w," Score:",score
    #print len(results)
    #print results
    rendered = ""

    create(path)

    with open(path, 'w') as filehandle:  
        for listitem in results:
            filehandle.write('%s\n' % listitem)


    path = "results_en/"

    
#print results

