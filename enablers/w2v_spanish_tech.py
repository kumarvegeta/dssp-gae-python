# This Python file uses the following encoding: utf-8

import os
import codecs
import nltk
from nltk import word_tokenize, sent_tokenize
import gensim
from gensim.models.word2vec import Word2Vec

spanish_tech_repo = "wiki_es_tech"

spanish_tech_model_path = "Spanish_Technology.w2v"

#nltk.download('all')

def get_sentences(repo=spanish_tech_repo):

    sentences = []

    for document in os.listdir(spanish_tech_repo):

        doc_path = os.path.join(spanish_tech_repo, document)
        print("Extracting for %s ...." % doc_path)
        content = codecs.open(doc_path, "r", "utf-8-sig").read()
        for sentence in nltk.sent_tokenize(content):
            sentences.append(nltk.word_tokenize(sentence))
    return sentences


def get_model(model_path=spanish_tech_model_path):
    if os.path.exists(model_path):
        print("Using existing model ... ")
        return gensim.models.Word2Vec.load(model_path)
    spanish_sentences = get_sentences()
    print("Building Model ..... ")
    model = Word2Vec(sentences=spanish_sentences, size=64, sg=1, window=10, min_count=5, seed=42, workers=8)
    model.save(model_path)
    print("Model saved to %s .... " % model_path)
    return model

spanish_tech_model = get_model()

spanish_tech_model.most_similar('palabra')



