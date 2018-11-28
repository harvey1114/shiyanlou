import pandas as pd

def co2():
    df_climate = pd.read_excel('ClimateChange.xlsx',sheetname='Data')
    df_co2 = df_climate[df_climate['Series code']=='EN.ATM.CO2E.KT'].replace({'..':float('nan')})

    df_co2 = df_co2.drop(['Country name','Series code','Series name','SCALE','Decimals'],axis=1)
    df_co2.set_index('Country code',inplace=True)

    df_co2 = df_co2.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    df_co2 = df_co2.dropna(how='all')
    df_co2['Sum emissions'] = df_co2.apply(lambda x : x.sum(),axis=1)
    df_co2 = df_co2['Sum emissions']#[df_co2['Sum emissions']!=0]
    df_country = pd.read_excel('ClimateChange.xlsx',sheetname='Country')
    df_country.set_index('Country code',inplace=True)
    df_country = df_country[['Country name','Income group']]
    df_concat = pd.concat([df_co2,df_country],axis=1)
    sum_df = df_concat.groupby(['Income group']).sum()
    max_df = df_concat.sort_values(by='Sum emissions', ascending=False).groupby(
            'Income group').head(1).set_index('Income group')
    max_df.rename(columns={'Sum emissions':'Highest emissions','Country name':'Highest emission country'},inplace=True)
    min_df = df_concat.sort_values(by='Sum emissions').groupby(
            'Income group').head(1).set_index('Income group')
    min_df.rename(columns={'Sum emissions':'Lowest emissions','Country name':'Lowest emission country'},inplace=True)
    results = pd.concat([sum_df,max_df,min_df],axis=1)
    return results

if __name__ == '__main__':
    print(co2())
