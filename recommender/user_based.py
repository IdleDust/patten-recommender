#!/usr/bin/env python
# coding: utf-8

# In[28]:


"""
Input:
    user: string format user_id, eg:'yjuqle'
    clicks: dictionary, user clicks record, eg:
    {
    'qgjuc': {4886794, 5732480, 7072753, 7189198, 8006808, 8029913, 8419399},
    pwqvk': {4045704, 4176847}
    }

Function:
    search_similar_user(user, clicks)
    
"""
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix

patent_sample = pd.read_csv('recommender/Data/all_combined.csv').drop(['Unnamed: 0'], axis=1)
patent = list(patent_sample.columns)

"""
get user clicks sparse matrix
"""
def get_user_clicks_csr_matrix(patents, users):
    n_patents = len(patents)
    # print("n_patents: %d" %n_patents)
    n_users = len(users)
    data_lenth = 0
    indptr = [0]
    indices = np.array([])
    for user in users:
        data_lenth += len(clicks[user])
        indptr.append(len(clicks[user]) + indptr[-1])
        click_patents = []
        indexes = [i for i,x in enumerate(patents) if x in clicks[user]]
        indices = np.append(indices, np.array(indexes))
    indptr = np.array(indptr)    
    data = np.array([1] * data_lenth)
    clicks_matrix = csr_matrix((data, indices, indptr), shape=(n_users, n_patents))
    return clicks_matrix

"""
Compute pairwise pearson correlation of users
"""
def get_user_corr(clicks_matrix):
    df = pd.DataFrame(clicks_matrix.toarray().T)
    corr = df.corr()
    return corr

"""
get the most close neighbors (peason correlation > 0), if no similar neighbors, return []
recommend nearest neighbor's clicked patent to the user
"""
def user_based_recommender(user, clicks):

    users = list(clicks.keys())
    patents = list(patent_sample['id'])
    #patents = list(patent_sample.columns)

    clicks_matrix = get_user_clicks_csr_matrix(patents, users)
    corr = get_user_corr(clicks_matrix)

    ui = users.index(user)

    neighbors = [(i, x) for i,x in enumerate(corr[ui]) if x > 0 and i != ui]
    neighbors.sort(key=lambda x: x[1], reverse=True)
    
    if not neighbors or len(neighbors) == 0:
        return []
    nn = neighbors[0][0]
    recomm_list = [ x for x in clicks[users[nn]] if x not in clicks[user] ]
    
    return recomm_list

"""
get the result dataframe
"""
def search_similar_user(user, clicks):
    idlist = user_based_recommender(user, clicks)
    temp = patent_sample.copy()
    temp = temp[temp['id'].isin(idlist)]
    return temp

