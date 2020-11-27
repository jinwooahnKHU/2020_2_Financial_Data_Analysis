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


# In[53]:


def fixing_date(date_data):
    if '\xa0·\xa0' not in date_data:
        return date_data
    return date_data.replace('\xa0·\xa0',"")


# In[54]:


#startdate '02/01/2020'
#save_name  : 'hello'
def crawling_news(company_name_list, start_date, end_date, save_file_name):
    #set logger Handler
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)
    
    #define googlenews 
    googlenews = GoogleNews(lang = 'en', start = start_date, end = end_date , encode = 'utf-8')
    #news.google.com search sample
    all_title = []
    logging.info('loop start')
    for i in range(len(company_name_list)):
        comp_name = company_name_list[i]
        googlenews.search(comp_name)
        logging.info('%s : %d%s' % (comp_name, ((i + 1) / len(company_name_list))*100  , '%'))
        for j in range(len(googlenews.results())):
            temp = []
            temp.append(googlenews.results()[j].get('title'))
            temp.append(comp_name)
            temp.append(fixing_date(googlenews.results()[j].get('date')))
            all_title.append(temp)
        #clear result list
        googlenews.clear()
    all_title = pd.DataFrame(all_title)
    all_title.to_csv('%s.csv' % (save_file_name))
    logging.info('saved as %s.csv, done!!' % (save_file_name))
    return all_title


# In[ ]:


#특정기간동안 SP500 기업들의 이름으로 검색한 뉴스들의 헤드라인을 전부 긁기
sp500 = pd.read_csv('sp500list.csv')


# In[ ]:


splist = list(sp500['company_name'])


# In[55]:


crawling_news(apple, '08/01/2018','10/29/2018', 'apple_amazon')

