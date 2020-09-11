#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas_datareader.data as web
import matplotlib.pyplot as plt
#plot이 주피터 노트북에 바로 보이게 해줌
get_ipython().run_line_magic('matplotlib', 'inline')


# *** Retrieving Data from Yahoo Finance ***

# In[2]:


#Retrieving Data from Yahoo Finance
#microsoft data
#web으로 get하면 dataframe형태로 불러와지고 index type은 'Date'가 된다.
msft = web.get_data_yahoo('MSFT', start = '2020-01-01', end = '2020-09-01')
msft.head()


# In[3]:


msft.index


# In[4]:


#Plot
#가로 10, 세로 5 만큼의 사이즈 생성
plt.figure(figsize = (10,5))
#x축은 index, y축은 Close로 그래프 하나 그림
plt.plot(msft.index, msft.Close, label = 'Close')
#x축은 index, y축은 Adj Close로 그래프 하나 그림
plt.plot(msft.index, msft['Adj Close'], label = 'Adj Close')
#legend를 왼쪽위에 배치
plt.legend(loc = 'best')
#grid생성
plt.grid()


# In[5]:


#Stock Return
#'pct_change', 혹은 'Shift' 함수 사용.
msft_ret = msft['Adj Close'].pct_change()
msft_ret.head()
#na를 drop하려면 
#msft_ret = msft_ret.dropna(axis = 0)

#'Shift' 함수를 이용하는 방법
#Shift 함수는 index는 내버려 두고 데이터만 이동시킨다!!
#shift(1)은 데이터를 하나 밑으로 밀어내는 것.
#msft_ret = msft['Adj Close'] / msft['Adj Close'].shift(1) - 1


# In[6]:


#Plot Stock Return
plt.figure(figsize= (10,5))
plt.plot(msft.index, msft_ret, label = 'Return')
plt.legend(loc = 'best')
plt.grid()


# In[7]:


msft_ret.describe()


# *** Retrieving Data from FRED ***

# In[8]:


#DataReader을 사용해보자.
data = web.DataReader(['SP500', 'WILL5000INDFC'], 'fred', start = '2016-01-02', end = '2020-09-01')
data.columns = ['S&P500', 'WilShire5000']
data.head()


# In[14]:


#Plot and compare two indices
data.plot()
plt.legend(loc = 'best')
plt.grid()
#plt.show()는 그냥 공간만 보여준다는거인듯. 그래프를 보여주려면 plot이 필요.
plt.show()


# In[16]:


#둘의 지수가 다르니 비교하기 위해서 둘 다 시작을 100으로 맞춰서 증가 추이를 보자.
((data / data.iloc[0]) * 100).plot(figsize = (10,5))
plt.legend(loc = 'best')
plt.grid()
plt.show()


# In[17]:


#Retriving Home price
cs = web.DataReader('CSUSHPINSA', 'fred', start = '1990-01-01', end = '2020-09-01')
cs.head()


# In[20]:


cs.plot()
plt.grid()


# *** Retrieving Data from Kenneth R. French Data Library ***

# In[22]:


from pandas_datareader.famafrench import get_available_datasets


# In[23]:


get_available_datasets()


# In[24]:


ind = web.DataReader('5_industry_Portfolios', 'famafrench', start = '2000-01-01', end = '2020-09-01')
type(ind)


# In[26]:


#description 
print(ind['DESCR'])


# In[28]:


ind


# In[31]:


#Convert percentages to decimals
(ind[0] / 100).head()


# In[32]:


(ind[0] / 100).plot()


# *** Retrieving Data from Naver ***

# In[33]:


#삼성전자
df = web.DataReader('005930', 'naver', start = '2018-01-01', end = '2020-09-01')
df.head()


# In[34]:


df.Close.head()


# In[37]:


df.Close = df.Close.astype(float)


# In[38]:


df.Close.head()


# In[39]:


df.Close.plot()

