import sys
import json
import pandas as pd

def analysis(file,user_id):
    times = 0
    minutes = 0

    df = pd.read_json(file)

    times = len(df[df['user_id']==user_id])
    minutes = df[df['user_id']==user_id]['minutes'].sum()

    return times,minutes

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Parameter error')
    else:
        times,minutes = analysis(sys.argv[1],int(sys.argv[2]))
        print('times: {}, minutes: {}'.format(times,minutes))
