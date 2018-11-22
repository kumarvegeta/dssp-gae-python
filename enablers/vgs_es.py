#!/usr/bin/env python
# coding: utf-8

# In[43]:


from keras.models import Sequential
import nltk
from nltk import word_tokenize, sent_tokenize
import pandas as pd
from keras.datasets import reuters
#import keras.datasets.reuters

nltk.download('punkt')

nltk.download('gutenberg')

from nltk.corpus import gutenberg


# In[25]:


import gensim
from gensim.models.word2vec import Word2Vec
#from keras.datasets import  


# In[31]:


#gutenberg.fileids()
sent_tokenize(gutenberg.raw())
gberg_sents = gutenberg.sents()

len(gutenberg.words())


# In[45]:


word2index = reuters.get_word_index()
index2word = dict([(i,w) for (w,i) in word2index.items()])


# In[57]:


print(index2word[124])


# In[51]:


(x_train, y_train) = reuters.load_data()


# In[64]:



for i,j in x_train:
    print(i)
    print(type(i))
    for j in index2word:
           if int(i)+3 == j:
               print(j)


# In[27]:


model = Word2Vec(sentences=gberg_sents, size=64, sg=1, window=10, min_count=5, seed=42, workers=8)
model.save('raw_gutenberg_es_model.w2v')

#model = gensim.models.Word2Vec.load('raw_gutenberg_es_model.w2v')


# In[42]:


model.most_similar('amigo')

