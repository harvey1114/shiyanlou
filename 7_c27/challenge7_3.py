import numpy as np
import pandas as pd
from pandas import Series
from matplotlib import pyplot as plt

def climate_plot():
    gas_list= ['EN.ATM.CO2E.KT','EN.ATM.METH.KT.CE','EN.ATM.NOXE.KT.CE','EN.ATM.GHGO.KT.CE','EN.CLC.GHGR.MT.CE']
    df_climate = pd.read_excel("ClimateChange.xlsx", sheetname='Data')
    df_climate.drop(['Country name','Country code','Series name','SCALE','Decimals'],axis=1,inplace=True)
    df_climate = df_climate[df_climate['Series code'].isin(gas_list)][df_climate.columns[0:-1]]
    df_climate.set_index('Series code',inplace=True)
    df_climate.replace({'..':np.nan},inplace=True)
    df_climate = df_climate.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    df_climate = df_climate.dropna(how='all')
    df_climate = df_climate.groupby(['Series code']).sum()
    df_climate.loc['Total GHG'] = df_climate.apply(lambda x: x.sum())
    gas_sum = df_climate.loc['Total GHG']
    gas_sum = gas_sum.apply(lambda x : (x-gas_sum.min())/(gas_sum.max()-gas_sum.min()))

    df_temperature = pd.read_excel("GlobalTemperature.xlsx")
    df_temperature = df_temperature.drop(['Land Max Temperature','Land Min Temperature'],axis=1)
    df_temperature['Date'] = pd.to_datetime(df_temperature['Date'])
    df_temperature['Year'] = df_temperature['Date'].apply(lambda x: x.year)
    s = Series(gas_sum.index).apply(lambda x : int(x))
    df_t = df_temperature[df_temperature['Year'].isin(s)]
    df_t = df_t.groupby('Year').mean()
    lv = df_t['Land Average Temperature']
    lov = df_t['Land And Ocean Average Temperature']
    lv = lv.apply(lambda x : (x-lv.min())/(lv.max()-lv.min()))
    lov = lov.apply(lambda x : (x-lov.min())/(lov.max()-lov.min()))
    df1 = pd.concat([lv,lov,gas_sum],axis=1)

    df2 = df_temperature.set_index('Date').drop(['Year'],axis=1).resample('Q').mean()

    fig=plt.figure()
    ax1 = df1.plot(
        kind='line',
        ax=fig.add_subplot(2, 2, 1),
    )
    ax1.set_xlabel('Years')
    ax1.set_ylabel('Values')
    ax1.set_xticks(s[::2])
    ax1.set_xticklabels(s[::2])
    ax1.legend()
    

    ax2 = df1.plot(
        kind='bar',
        ax=fig.add_subplot(2, 2, 2),
    )
    ax2.set_xlabel('Years')
    ax2.set_ylabel('Values')
    ax2.legend()
    
    ax3 = df2.plot(
        kind='area',
        ax=fig.add_subplot(2, 2, 3),
    )
    ax3.set_xlabel('Quarters')
    ax3.set_ylabel('Temperature')
    ax3.legend()
    
    ax4 = df2.plot(
        kind='kde',
        ax=fig.add_subplot(2, 2, 4),
    )
    ax4.set_xlabel('Values')
    ax4.set_ylabel('Values')
    ax4.legend()
    plt.show()
    return fig

climate_plot()
