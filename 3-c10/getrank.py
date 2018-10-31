import sys
from pymongo import MongoClient

def get_rank(user_id):
    client = MongoClient('127.0.0.1',27017)
    db = client.shiyanlou
    contests = db.contests
    user_dict = {}
    users = contests.find()
    if db.tc.find():
        db.tc.drop()
    for user in users:
        if user['user_id'] in user_dict.keys():
            user_dict[user['user_id']][1] += user['score']
            user_dict[user['user_id']][2] += user['submit_time']
        else:
            list=[0,user['score'],user['submit_time']]
            user_dict[user['user_id']] = list
    #print(user_dict)
    for k,v in user_dict.items():
        db.tc.insert({'user_id':k,'score':v[1],'submit_time':v[2]})

    ordered_users = db.tc.find().sort([('score',-1),('submit_time',1)])
    #for ou in ordered_users:
    #    print(ordered_users)
    rank,score,submit_time=0,0,0
    for i,ou in enumerate(ordered_users):
        if ou['user_id'] == user_id:
            rank = i+1
            score = ou['score']
            submit_time = ou['submit_time']
    return rank,score,submit_time

if __name__ == '__main__':

    if len(sys.argv) == 2 and str(sys.argv[1]).isdigit():
        user_id = int(sys.argv[1])
    else:
        print("Parameter Error")
    
    #get_rank(user_id)
    userdata = get_rank(user_id)
    print(userdata)



