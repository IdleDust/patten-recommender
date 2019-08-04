#!/usr/bin/env python
# coding: utf-8

# In[91]:


'''
Instructions of functions:

tfidf_weighted_words(sentence) -- calculating tf-idf scores for an assigned word or a sentence. 
    Example: tfidf_weighted_words('bicycle')
             tfidf_weighted_words('big data analysis')
             
tfidf_similarity(patent_id) -- calculating the similarity for a patent. Input should be a patent id number. 
    Example: tfidf_similarity(10000000)

'''


# In[49]:


import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import threading

# In[36]:


# df = pd.read_csv("recommender/Data/all_combined.csv").drop(['Unnamed: 0'], axis=1)
# dftx = pd.read_csv("recommender/Data/tfidf-title.csv").drop(['Unnamed: 0'], axis=1)
# dftx1 = pd.read_csv("recommender/Data/tfidf-abstract.csv").drop(['Unnamed: 0'], axis=1)
# tfidf = pd.read_csv("recommender/Data/tfidf-title-combined.csv").drop(['Unnamed: 0'], axis=1)
# tfidf1 = pd.read_csv("recommender/Data/tfidf-abstract-combined.csv").drop(['Unnamed: 0'], axis=1)

df = None
dftx = None
dftx1 = None
tfidf = None
tfidf1 = None

df_file = "recommender/Data/all_combined.csv"
dftx_file = "recommender/Data/tfidf-title.csv"
dftx1_file = "recommender/Data/tfidf-abstract.csv"
tfidf_file = "recommender/Data/tfidf-title-combined.csv"
tfidf1_file = "recommender/Data/tfidf-abstract-combined.csv"


def read_file_from_csv(file_descriptor, file_name):
    file_descriptor = pd.read_csv(file_name).drop(['Unnamed: 0'], axis=1)


data_file = [(df, df_file), (dftx, dftx_file), (dftx1, dftx1_file), (tfidf, tfidf_file), (tfidf1, tfidf1_file)]


from multiprocessing import Process

idx = 1
for x in data_file:
    t = threading.Thread(target=read_file_from_csv(x[0], x[1]), name='thread{0}'.format(idx))
    idx = idx + 1
    t.start()
    t.join()
    print("thread %s ended" % threading.current_thread().name)
    # print("len of df {0}".format(len(df)))
    # p=Process(target=read_file_from_csv, args=(x[0], x[1],))
    # p.start()
    # p.join()




# In[93]:


sim_t = cosine_similarity(dftx)
sim_a = cosine_similarity(dftx1)
word_list_title = dftx.columns.get_values().tolist()
word_list_abstract = dftx1.columns.get_values().tolist()




# In[95]:


def tfidf_weighted(word):
    temp = df.copy()
    word = word.lower()
    
    if word in word_list_abstract:
        temp_a = tfidf1.sort_values(by=word , ascending=False)[[word]]
        temp['result_a'] = temp_a[[word]]
    else:
        temp['result_a'] = 0.0
        
    if word in word_list_title:
        temp_t = tfidf.sort_values(by=word , ascending=False)[[word]]
        temp['result_t'] = temp_t[[word]]
    else:
        temp['result_t'] = 0.0
    
    temp['result_weighted'] = 0.8 * temp['result_t'] + 0.2 * temp['result_a']
    temp = temp.sort_values(by=['result_weighted'] , ascending=False)
    #temp = temp[(temp['result_weighted'] > 0)]
    temp = temp.drop(columns=['result_t', 'result_a'])
    
    return temp

def tfidf_weighted_words(sentence):
    wordlist = re.sub("[^\w]", " ",  sentence).split()
    temp = pd.DataFrame()
    for i in range(len(wordlist)):
        temp[wordlist[i]] = tfidf_weighted(wordlist[i])['result_weighted']
    
    temp.loc[:,'Total'] = temp.sum(axis=1)
    temp = temp[['Total']]
    
    res = pd.concat([df, temp], axis=1).sort_values(by="Total" , ascending=False)
    res = res[(res['Total'] > 0)]
    return res


# In[102]:


def tfidf_similarity(patent_id):
    temp = df.copy()
    index = temp[temp['id']==patent_id].index.values.astype(int)[0]
    temp['sim_temp_t'] = sim_t[index]
    temp['sim_temp_a'] = sim_a[index]
    temp['sim_temp'] = 0.8 * temp['sim_temp_t'] + 0.2 * temp['sim_temp_a']
    temp = temp.sort_values(by="sim_temp" , ascending=False)
    temp = temp[(temp['sim_temp'] > 0)]
    temp = temp[1:6]
    temp = temp.drop(columns=['sim_temp_t', 'sim_temp_a'])
    
    return temp


# In[ ]:



