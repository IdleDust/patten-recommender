#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import pandas as pd
import numpy as np
import re
import nltk

# content-based method pre-processing: cb_download()
# knowledge-based method pre-processing: kb_download()


# In[1]:


def cb_download():
    df = pd.read_csv("Data/all_combined.csv").drop(['Unnamed: 0'], axis=1)
    dft = df.copy()
    stop = stopwords.words('english')

    dft['title'] = dft['title'].str.replace('\d+', '')
    dft['title'] = dft['title'].str.split(' ').apply(lambda x: [item for item in x if item not in stop])
    dft['title']=dft['title'].apply(', '.join)
    v = TfidfVectorizer()
    x = v.fit_transform(dft['title'])
    dftx = pd.DataFrame(x.toarray(), columns=v.get_feature_names())
    tfidf= pd.concat([df, dftx], axis=1)

    dft['abstract'] = dft['abstract'].str.replace('\d+', '')
    dft['abstract'] = dft['abstract'].str.split(' ').apply(lambda x: [item for item in x if item not in stop])
    dft['abstract'] = dft['abstract'].apply(', '.join)
    x1 = v.fit_transform(dft['abstract'])
    dftx1 = pd.DataFrame(x1.toarray(), columns=v.get_feature_names())
    tfidf1= pd.concat([df, dftx1], axis=1)
    
    sim_t = cosine_similarity(dftx)
    sim_a = cosine_similarity(dftx1)
    word_list_title = dftx.columns.get_values().tolist()
    word_list_abstract = dftx1.columns.get_values().tolist()


# In[2]:


def kb_download():
    dfk = pd.read_csv("Data/all_combined.csv").drop(['Unnamed: 0'], axis=1)
    inv = pd.read_csv("Data/inv_cleaned.csv").drop(['Unnamed: 0'], axis=1)
    law = pd.read_csv("Data/law_cleaned.csv").drop(['Unnamed: 0'], axis=1)
    asi = pd.read_csv("Data/asi_cleaned.csv").drop(['Unnamed: 0'], axis=1)


if __name__ == '__main__':
    nltk.download()
