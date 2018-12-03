import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import linear_model


def Temperature():
    gh_gas = pd.read_csv("GreenhouseGas.csv")
    co2_ppm = pd.read_csv("CO2ppm.csv")
    gs_temperature = pd.read_csv("GlobalSurfaceTemperature.csv")

    gh_gas = gh_gas.set_index('Year')
    co2_ppm = co2_ppm.set_index('Year')
    gs_temperature = gs_temperature.set_index('Year')
    df = pd.concat([gh_gas,co2_ppm,gs_temperature],axis=1).fillna(method='ffill').fillna(method='bfill').reset_index()
    data_range = np.arange(1970,2010)
    test_range = np.arange(2011,2018)
    df_data = df[df['Year'].isin(data_range)].iloc[:,1:]
    df_predict_x = df[df['Year'].isin(test_range)].iloc[:,1:-3]

    x=[]
    x_predict=[]
    ym,yu,yl=[],[],[]
    for index,row in df_data.iterrows():
        x.append(row[0:4])
        ym.append(row[4])
        yu.append(row[5])
        yl.append(row[6])
    for index,row in df_predict_x.iterrows():
        x_predict.append(row[:])
    

    model_m = linear_model.LinearRegression()
    model_m.fit (x,ym)
    model_u = linear_model.LinearRegression()
    model_u.fit (x,yu)
    model_l = linear_model.LinearRegression()
    model_l.fit (x,yl)

    MedianPredict = [float('{:.3f}'.format(x)) for x in model_m.predict(x_predict)]
    UpperPredict = [float('{:.3f}'.format(x)) for x in model_u.predict(x_predict)]
    LowerPredict = [float('{:.3f}'.format(x)) for x in model_l.predict(x_predict)]

    print(MedianPredict)
    print(UpperPredict)
    print(LowerPredict)

    return UpperPredict,MedianPredict,LowerPredict

Temperature()
