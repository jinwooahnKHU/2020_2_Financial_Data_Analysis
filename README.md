# 2020_2_Financial_Data_Analysis

+ Codes used in Financial Data Analysis class

## 개요

### 목적

+ 미국 시장에 투자하고 싶은 고객에게, 감성분석을 통해 해당 유니버스 내에서 긍정적인 기사의 비율이 높은 회사를 선택하여 동등한 risk를 가지도록 포트폴리오를 구성해준다.

<img src ="https://user-images.githubusercontent.com/48755376/156698197-2363924f-acac-49e9-9fad-2ef6a59c1b84.png" width = "1200" height = "600">


### 포트폴리오 전략

1. 종목 선택

+ universe : S&P 500

2. 감성분석(sentiment analysis)

+ 매 투자일을 매월 1일이라고 했을 때, 그 전 한달동안의 기업들에 대한 기사를 수집 → 토큰화 → 하버드 감성사전을 이용해 긍정 단어 출현 비율이 높은 top 10개 회사를 선정한다

3. 포트폴리오 가중치 부여

+ risk parity 전략 사용

### Risk Parity

+ 포트폴리오를 구성하는 자산들의 리스크를 동등하게 구성

<img width="383" alt="risk" src="https://user-images.githubusercontent.com/48755376/156698734-2408ae15-38e0-4e5e-bc52-877c37014ce0.png">



### 백테스트

+ 평가 기준 : Expected Return, volatility, Maximum Draw Down

