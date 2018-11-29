# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import Series

def analyze_data(series_code):
    df_climate = pd.read_excel("ClimateChange.xlsx", sheetname='Data')
    df = df_climate[df_climate['Series code']==series_code].replace({'..':float('nan')})

    df = df.drop(['Country name','Series code','Series name','SCALE','Decimals'],axis=1)
    df.set_index('Country code',inplace=True)

    df = df.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    df = df.replace({float('nan'):0})
    df['Sum'] = df.apply(lambda x : x.sum(),axis=1)
    
    s = df['Sum']
    df['Sum'] = Series([(x-s.min())/(s.max()-s.min()) for x in df['Sum']],index=df.index)
    df_data = df['Sum']
    
    return df_data

def co2_gdp_plot():

    df_co2 = analyze_data('EN.ATM.CO2E.KT').rename('Co2 Sum')
    df_gdp = analyze_data('NY.GDP.MKTP.CD').rename('Gdp Sum')

    df = pd.concat([df_co2,df_gdp],axis=1)
    
    
    c_list = ['CHN', 'USA', 'GBR', 'FRA','RUS']
    c_country = ['CHN', 'USA', 'GBR', 'FRA','RUS']
    c_position = []
    for i,index in enumerate(df.index):
        if len(c_list)>0 and index in c_list:
            c_position.append(i)
            c_list.remove(index)

    china_sum = df.iloc[c_position[0]]
    china=[np.round(china_sum['Co2 Sum'],3),np.round(china_sum['Gdp Sum'],3)]
    fig = plt.subplot()
    plt.title('GDP-CO2')
    plt.xlabel('Countries')
    plt.ylabel('Values')
    plt.plot(range(len(df.index)),df['Co2 Sum'],'b-',label='CO2-SUM')
    plt.plot(range(len(df.index)),df['Gdp Sum'],'r-',label='GDP-SUM')
    plt.xticks(c_position,c_country,rotation='vertical')

    plt.legend()
    plt.show()
    return fig, china

_,china = co2_gdp_plot()
print(china)
