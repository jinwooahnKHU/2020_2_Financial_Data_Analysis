#!/usr/bin/env python
# coding: utf-8

# In[1]:


import bs4 as bs
import pickle
import requests


# In[31]:


def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    tickers_1 = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text[:-1]
        tickers.append(ticker)
    
    for row in table.findAll('tr')[1:]:
        ticker_1 = row.findAll('td')[1].text[:-1]
        tickers_1.append(ticker_1)
        
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)
        
    return  tickers_1, tickers


# In[32]:


company_name, code =  save_sp500_tickers()


# In[19]:


import pandas as pd
import numpy as np


# In[35]:


company_name = pd.DataFrame(company_name)
code = pd.DataFrame(code)


# In[41]:


sp500list = pd.concat([company_name, code], axis =1)


# In[43]:


sp500list.columns = ['company_name', 'code']


# In[45]:


sp500list.to_csv('sp500list.csv')

