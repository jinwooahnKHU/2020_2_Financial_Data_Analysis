#!/usr/bin/env python
# coding: utf-8

# In[66]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


import pandas_datareader as web


# ***Return Distribution with Amazon ***

# In[3]:


amzn = web.get_data_yahoo('AMZN', start = '2000-01-01', end = '2020-09-01')
amzn.head()


# In[4]:


#수익률 계산
amzn_ret = amzn['Adj Close'].pct_change()


# In[5]:


amzn_ret.head()


# In[6]:


#NA를 제거하고 update해서 저장
amzn_ret.dropna(inplace = True)
amzn_ret.head()


# In[7]:


amzn_ret.describe()


# *** Plot returns along with average ***

# In[10]:


plt.figure(figsize = (15,5))
plt.plot(amzn_ret.index, amzn_ret, label = 'Return', zorder = 0)
#평균으로 수평선 그리기 zorder = 1 : 빨간선을 파란선 위에 그리겟다는 뜻인듯?
plt.hlines(amzn_ret.mean(), amzn_ret.index[0], amzn_ret.index[-1], label = 'Mean', color = 'r', zorder = 1)
plt.legend(loc = 'best')
plt.grid()


# In[12]:


#Plot historgram using Seaborn
import seaborn as sns
import scipy as sp


# In[14]:


#kde =false : 밀도 그래프를 그리지 않는다. 
#fit = sp.stats.norm : 정규분포와 비교함
sns.distplot(amzn_ret, kde = False, fit = sp.stats.norm)


# In[17]:


#Plot histogram with including rugplot
#rug plot을 포함시켜서 값들이 어디에 분포하는지 알 수 있다.
sns.distplot(amzn_ret, rug = True, kde = False, fit = sp.stats.norm)


# In[18]:


#Check Skewnewss and Kurtosis using Scipy
sp.stats.skew(amzn_ret), sp.stats.kurtosis(amzn_ret)


# *** Using Q-Q plot to compare with normal distribution ***

# In[22]:


#subplot() : 여러개의 그래프를 그리기 위함
ax = plt.subplot()
sp.stats.probplot(amzn_ret, plot = ax)
plt.show()


# In[24]:


#S&P500으로 Q-Q plot 비교
sp500 = web.get_data_yahoo('^GSPC', start = '2000-01-01', end = '2020-09-01')
ax = plt.subplot()
sp.stats.probplot(sp500['Adj Close'].pct_change().dropna(), plot = ax)
plt.show()


# *** Normality Test using K-S and J-B tests ***

# In[25]:


#K - S Test
#다른 dist와 비교하는 것이기에 비교 dist가 input으로 들어가야함
sp.stats.kstest(amzn_ret, 'norm')


# In[26]:


sp500_ret = sp500['Adj Close'].pct_change().dropna()
sp.stats.kstest(sp500_ret, 'norm')


# In[27]:


#J-B Test
#normality 만 검증하기 때문에 input이 더 필요없고 return만 넣어주면됨
sp.stats.jarque_bera(amzn_ret)


# In[28]:


sp.stats.jarque_bera(sp500_ret)


# *** Correlation of Assets ***

# In[29]:


#Use 5 industry portfolios(devides the stock market into 5 industries)
ind5 = web.DataReader('5_Industry_Portfolios', 'famafrench', start = '1990-01-01', end = '2020-09-01')


# In[33]:


#fama french에서 불러오는건 dict형태라서 pct_change함수를 사용할 수 없음!!
ind5_ret = ind5[0] / 100
ind5_ret.head()


# In[34]:


ind5_ret.corr()


# In[35]:


#Correlation Visualization using a heatmap( using matplotlib pyplot)
plt.matshow(ind5_ret.corr())
plt.colorbar()


# In[36]:


#Correlation Visualization heatmap using seaborn
#annot = True : 값 표시
sns.heatmap(ind5_ret.corr(), annot = True)


# In[37]:


# 금융위기 상황에서의 correlation
#Global finance crisis 2008
crisis1 = ind5_ret.loc['2007-01':'2008-12']
sns.heatmap(crisis1.corr(), annot = True)
#=> 전반적으로 산업군들의 상관관계가 높아진다!


# In[38]:


#Global finance crisis with Covid-19
crisis2 = ind5_ret.loc['2020-01' : '2020-9']
sns.heatmap(crisis2.corr(), annot = True)


# In[39]:


#많은 산업군으로 비교할수록 차이는 더 극명해진다.
#10 Industry Porfolios
ind10 = web.DataReader('10_Industry_Portfolios', 'famafrench', start = '1990-01-01', end = '2020-09-01')
ind10_ret = ind10[0]/100
ind10_ret.head()


# In[41]:


sns.heatmap(ind10_ret.corr(), annot = True)


# *** High Volatility ***
# 변동성이 큰 시기에 자산, 산업들의 상관관계가 높아진다
# 그렇다면 변동성은 어떻게 측정할 것인가?
# => 변동성만 나타내는 지수가 있다  : 'VIX'

# In[45]:


vix = web.get_data_yahoo('^VIX', start = '2000-01-01', end = '2020-09-01')
vix.head()


# In[46]:


plt.figure(figsize = (10,5))
plt.plot(vix.index, vix.Close)
plt.grid()


# *** Exercise ***
# 주식의 수익률이 Skewed되어있을 떄 trimmed average를 계산하고 싶다.
# trimmed average : outlier 때문에 평균이 영향을 받을 떄 outlier 영향을 받지 않는 평균
#     => outlier 빼고 나머지 값으로 계산한다.

# In[47]:


sp500 = web.get_data_yahoo('^GSPC', start = '1990-01-01', end = '2020-09-01')['Adj Close'].pct_change().dropna()


# In[48]:


sp500.head()


# In[51]:


# sort 하기
sp500_sort = sp500.sort_values()
sp500_sort.head()


# In[53]:


sp500_sort.shape


# In[54]:


n = sp500_sort.shape[0]


# In[56]:


#Check the histogram and mean returns
sns.distplot(sp500_sort, rug = True, kde = False, fit = sp.stats.norm)


# In[59]:


print('Daily mean : %.3f%%' % (sp500_sort.mean()*100))
print('Annualized mean : %.3f%%' % (sp500_sort.mean()*252*100))


# In[61]:


means = pd.Series(sp500_sort.mean(), index = [0])
means


# In[62]:


for i in range(100):
    means[i + 1] = sp500_sort[i + 1 : -(i + 1)].mean()
means.tail()


# In[63]:


plt.plot(means)


# In[64]:


plt.plot(means * 252)


# In[67]:


#Numpy arrays를 사용하여 구하는 방식
#size 100이고 nan값으로 구성된 배열생성
means_np = np.full(100, np.nan)
for i in range(1,101):
    means_np[i-1] = sp500_sort[i : -i].mean()
means_np


# In[70]:


#Scipy trim_mean을 사용
#prop1 : [0/n, 1/n... 100 / n] n = 앞에서 정의한 변수(sp500_sort의 총 행 갯수)
#비율 변환해준거임
prop1 = np.arange(0,101) / n
trim1 = np.full(100, np.nan)
for i in range(100):
    trim1[i] = sp.stats.trim_mean(sp500_sort, prop1[i])
plt.plot(trim1)


# In[71]:


#trimming using proportion
#linspace : 시작과 끝을 넣고 그 사이를 동일한 구간으로 쪼개줌(stat, end, stepsize)
prop2 = np.linspace(0,100/n, 100)
trim2 = np.full(prop2.shape[0], np.nan)
for i in range(prop2.shape[0]):
    trim2[i] = sp.stats.trim_mean(sp500_sort, prop2[i])
plt.plot(trim2)

