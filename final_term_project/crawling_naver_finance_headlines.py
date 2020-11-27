#!/usr/bin/env python
# coding: utf-8

# In[52]:


""" 주식종목 뉴스(네이버 파이넌스) Crawling 하기 """  
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os 
import datetime


# In[54]:


#수집기간 정의
def datetime_list(start_date, end_date):
    days_range = []
    start = datetime.datetime.strptime(str(start_date), "%Y-%m-%d")
    end = datetime.datetime.strptime(str(end_date), "%Y-%m-%d") # 범위 + 1
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    for date in date_generated:
        days_range.append(date.strftime("%Y-%m-%d"))
    return days_range


# In[109]:



os.chdir('C:\\Users\\DrHyeonJin\\2020_second_semester\\FinanacialDataAnalysis\\term_project\\final_termproject')
def crawler(company_code, maxpage, date_list):
   
   page = 1 
   
   while page <= int(maxpage): 
   
       url = 'https://finance.naver.com/item/news_news.nhn?code=' + str(company_code) + '&page=' + str(page) 
       source_code = requests.get(url).text
       html = BeautifulSoup(source_code, "lxml")
        
           
       # 뉴스 제목 
       titles = html.select('.title')
       title_result=[]
       for title in titles: 
           title = title.get_text() 
           title = re.sub('\n','',title)
           title_result.append(title)

       # 뉴스 링크
       links = html.select('.title') 
        
       link_result =[]
       for link in links: 
           add = 'https://finance.naver.com' + link.find('a')['href']
           link_result.append(add)

       # 뉴스 날짜 
       dates = html.select('.date') 
       date_result = [date.get_text().replace('.','-')[1:11] for date in dates]
       
        
       # 뉴스 매체     
       sources = html.select('.info')
       source_result = [source.get_text() for source in sources] 
        
       page += 1
       
       # 변수들 합쳐서 해당 디렉토리에 csv파일로 저장하기 
   
   
   result= {"날짜" : date_result, "언론사" : source_result, "기사제목" : title_result, "링크" : link_result} 
   df_result = pd.DataFrame(result)
   df_result = df_result[df_result['날짜'].isin(date_list)]
   
       
   print("다운 받고 있습니다------")
   df_result.to_csv('page' + str(page) + 'c' + str(company_code) + '.csv', mode='w', encoding='utf-8-sig') 
            


# In[110]:


data = pd.read_csv('company_list.txt', dtype=str, sep='\t')
data = data.iloc[:2]


# In[112]:


target_code = list(data['종목코드'])


# In[113]:


date_list = datetime_list('2020-08-01', '2020-10-31')


# In[114]:


for i in range(len(target_code)):
    crawler(target_code[i],1, date_list)

