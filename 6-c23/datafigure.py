import pandas as pd
from matplotlib import pyplot as plt

def get_time(filepath):
    minutes = 0
    df = pd.read_json(filepath)
    id_list = list(set(df['user_id']))
    id_list.sort()
    minutes_list=[]
    for user_id in id_list:
        minutes = df[df['user_id']==user_id]['minutes'].sum()
        minutes_list.append(minutes)
    return id_list,minutes_list


def data_plot():

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_title('StudyData')
    ax.set_xlabel('User ID')
    ax.set_ylabel('Study Time')
    ax.plot(ids,minutes)
    
    plt.show()
    return ax


if __name__ == '__main__':
    ids,minutes = get_time('/home/shiyanlou/Code/user_study.json')
    data_plot()
