# This Python file uses the following encoding: utf-8

import numpy as np
import os
import operator
import pickle
from scipy.spatial.distance import cosine
from scipy.sparse import csr_matrix


VOCABULARY_FILE = 'vocabulary_spanish.pkl'
REVERSE_VOCABULARY_FILE = 'reverse_vocabulary_spanish.pkl'
COUNT_VECTORIZER_FILE = 'count_vectorizer_spanish.pkl'
TF_IDF_MATRIX_FILE = 'tf_idf_matrix_spanish.pkl'
WORD_VECTORS_FILE = 'results_es/word_vectors.pkl'
WORD_DISTANCES_FILE = 'results_es/word_distances.pkl'
SORTED_WORD_DISTANCES_FILE = 'results_es/sorted_word_distances.pkl'


def load_file(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)


def save_file(obj, file_name):
    with open(file_name, 'wb') as f:
        pickle.dump(obj, f)


def load_vectors_map():
    if os.path.isfile(WORD_VECTORS_FILE):
        return load_file(WORD_VECTORS_FILE)
    vocabulary = load_file(VOCABULARY_FILE)
    tf_idf_matrix = load_file(TF_IDF_MATRIX_FILE)
    vectors_map = {}
    print "Creating word vectors ... "
    for i, word in enumerate(vocabulary.keys()):
        if i % 1000 == 0:
            print i
        word_index = vocabulary[word]
        vector = np.array(csr_matrix(tf_idf_matrix[:, word_index]).todense())
        vectors_map[word] = vector
    print len(vectors_map)
    print "Finished creating word vectors!"
    save_file(vectors_map, WORD_VECTORS_FILE)
    return vectors_map


def make_reverse_vocabulary():
    if os.path.isfile(REVERSE_VOCABULARY_FILE):
        return load_file(REVERSE_VOCABULARY_FILE)
    vocabulary = load_file(VOCABULARY_FILE)
    reverse_vocabulary = {}
    print "Creating reverse vocabulary ... "
    for word, i in vocabulary.items():
        if i % 1000 == 0:
            print i
        reverse_vocabulary[i] = word
    save_file(reverse_vocabulary, REVERSE_VOCABULARY_FILE)
    return reverse_vocabulary


def process_new():
    base_path = "results_es/word_scores"
    nearest_words_path = "results_es/nearest_words"
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    if not os.path.exists(nearest_words_path):
        os.makedirs(nearest_words_path)
    distance_map = {}
    vectors_map = load_vectors_map()
    print "Size of Vocabulary = %d" % len(vectors_map)
    words = vectors_map.keys()
    print "Computing word distance scores ... "
    for i in range(len(words) - 1):
        word_i = words[i]
        score_path = "%s/%s.pkl" % (base_path, word_i)
        nearest_word_path = "%s/%s.pkl" % (nearest_words_path, word_i)
        if os.path.isfile(score_path):
            if i % 10 == 0:
                print "Scores for %d words" % i
            word_i_scores = load_file(score_path)
            for word_j, score in word_i_scores.items():
                word_j_scores = distance_map.get(word_j, {})
                word_j_scores[word_i] = score
                distance_map[word_j] = word_j_scores
            if word_i in distance_map:
                del distance_map[word_i]
            # distance_map[word_i] = load_file(score_path)
        else:
            if i % 10 == 0:
                print "Finished for %d words ... " % i
            for j in range(i + 1, len(words)):
                word_j = words[j]
                score = cosine(vectors_map[word_i], vectors_map[word_j])
                if score != 1.0 and score != 0.0 and score >= 0.9:
                    word_i_scores = distance_map.get(word_i, {})
                    word_i_scores[word_j] = score
                    distance_map[word_i] = word_i_scores
                    word_j_scores = distance_map.get(word_j, {})
                    word_j_scores[word_i] = score
                    distance_map[word_j] = word_j_scores
            save_file(distance_map.get(word_i, {}), score_path)
            nearest_words = sorted(distance_map.get(word_i, {}).items(), key=operator.itemgetter(1), reverse=True)
            save_file(nearest_words, nearest_word_path)
            if word_i in distance_map:
                del distance_map[word_i]  # Freeing memory
    print "Finished computing word distances!"
    print "Done!!"

make_reverse_vocabulary()
process_new()
