# -*- coding: utf-8 -*-
import sys
import getopt
import configparser
import csv
from datetime import datetime
from multiprocessing import Process,Queue,Pool


def parserargs():
    shortargs = 'C:c:d:o:h'
    longargs = ['help']
    opts,args = getopt.getopt(sys.argv[1:],shortargs,longargs)
    adict = {}
    for i,j in opts:
        if i in ('-h','--help'):
            print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')
            sys.exit()
        else:
            adict[i] = j
    return adict,args
            
    
def parserconfig(section):
    config = configparser.ConfigParser()
    config.read(args_dict['-c'],encoding='utf-8')
    s = section.upper()
    r = config.options(s)
    cdict = {}
    for i in r:
        cdict[i] = config.get(s,i)
    return cdict    


def _read_users_data(q1):
    userdata = []
    data_path = args_dict['-d']
    with open(data_path,'r') as f:
        for line in f.readlines():
            t = (line.split(',')[0].strip(),line.split(',')[1].strip())
            userdata.append(t)
    q1.put(userdata)

def cal_salary(nid,salary):
    salary = int(salary)
    salary_list = [nid,salary]
    p = 0.00
    insure = 0.00
    min_s = float(config_dict['jishul'])
    max_s = float(config_dict['jishuh'])
    for key,value in config_dict.items():
        
        if key == 'jishul' or key == 'jishuh':
            continue
        else:
            p += float(value)
    #print(p)
    if salary < min_s:
        insure = min_s * p
    elif salary > max_s:
        insure = max_s * p
    else:
        insure = salary *p
    salary_list.append('%.2f'%insure)
    s1 = salary - insure - 3500
    ratio,extra = 0.00,0
    if s1 <=1500: 
        ratio = 0.03
        extra = 0
    elif s1 <= 4500:
        ratio = 0.10
        extra = 105
    elif s1 <= 9000:
        ratio = 0.20
        extra = 555
    elif s1 <= 35000:
        ratio = 0.25
        extra = 1005
    elif s1 <= 55000:
        ratio = 0.30
        extra = 2755
    elif s1 <= 80000:
        ratio = 0.35
        extra = 5505
    else:
        ratio = 0.45
        extra = 13505
    
    tax = s1 * ratio - extra
    if tax < 0:
        tax = 0    
    salary_list.append('%.2f'%tax)
    final_salary = salary-insure-tax
    salary_list.append('%.2f'%final_salary)
    d = datetime.now()
    s = d.strftime('%Y-%m-%d %H:%M:%S')
    salary_list.append(s)
    return salary_list
    


def calc_for_all_userdata(q1,q2):
    result = []
    ulist = q1.get()
    for user in ulist:
        result.append(cal_salary(user[0],user[1]))
    q2.put(result)

def export(q2,default='csv'):
    result = q2.get()
    with open(args_dict['-o'],'w') as f:
        writer = csv.writer(f)
        writer.writerows(result)


if __name__ == '__main__':
    args_dict,largs = parserargs()
    config_dict = parserconfig(args_dict['-C']) 
    queue1 = Queue()
    queue2 = Queue()
    Process(target=_read_users_data,args=(queue1,)).start()
    Process(target=calc_for_all_userdata,args=(queue1,queue2)).start()
    Process(target=export,args=(queue2,)).start()
