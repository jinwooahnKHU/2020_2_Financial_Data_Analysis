#!/usr/bin/env python
# coding: utf-8

# In[1]:


from GoogleNews import GoogleNews


# In[2]:


import pandas as pd
import numpy as np


# 원하는 것 : 내가 투자하고 싶은 시기의 3개월 전의 S&P500 기업 리스트에 관한 뉴스 헤드라인을 쫙 모아 
#     => 감성사전으로 입혀서 indexing을 해 => LSTM훈련을 시킨다던지... 

# In[3]:


import logging
logging.basicConfig(level=logging.INFO)


# In[4]:


#startdate '02/01/2020'
def crawling_news(company_name_list, start_date, end_date):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)
    
    googlenews = GoogleNews()
    googlenews.set_lang('en')
    googlenews.set_time_range('start_date','end_date')
    googlenews.set_encode('utf-8')
    #news.google.com search sample
    all_title = []
    logging.info('loop start')
    for i in range(len(company_name_list)):
        googlenews.get_news(company_name_list[i])
        logging.info('%s : %0.2f%s' % (company_name_list[i], ((i + 1) / len(company_name_list))*100  , '%'))
        for j in range(len(googlenews.results())):
            all_title.append(googlenews.results()[j].get('title'))
    all_title = pd.DataFrame(all_title)
    all_title.to_csv('sp500news.csv')
    logging.info('saved to csv, done!!')
    return all_title


# In[32]:


#특정기간동안 SP500 기업들의 이름으로 검색한 뉴스들의 헤드라인을 전부 긁기
sp500 = pd.read_csv('sp500list.csv')


# In[44]:


splist = list(sp500['company_name'])


# In[5]:


splist_2 = ['Apple', 'Amazon']


# In[6]:


splist_news = crawling_news(splist_2, '08/01/2010','10/28/2010')


# In[49]:


len(splist)


# In[58]:


splist_news = crawling_news(splist, '08/01/2020','10/31/2020')

