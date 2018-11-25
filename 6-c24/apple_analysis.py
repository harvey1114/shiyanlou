import pandas as pd

def quarter_volume():
    data = pd.read_csv('apple.csv',header=0)
    data = data.drop(['Open','High','Low','Close'],axis=1)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date',inplace=True)
    data_sum = data.resample('Q').sum()
    ds = data_sum.sort_values(by='Volume',ascending=False)
    second_volume = ds.iloc[1]['Volume']
    return second_volume

if __name__ == '__main__':
    sv = quarter_volume()
    print(sv)
