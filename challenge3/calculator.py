# -*- coding: utf-8 -*-
import sys
import csv

class Args(object):
    def __init__(self):
        self.args = sys.argv[1:]

    @staticmethod
    def get_args(args):
        args_dict={}
        if len(args) == 7 and args[1] == '-c' and args[3] == '-d' and args[5] == '-o':
            args_dict['config_path'] = args[2]
            args_dict['data_path'] = args[4]
            args_dict['output_path'] = args[6]
            return args_dict
        else:
            print("Parameter ERROR")
            sys.exit(-1)


class Config(object):
    def __init__(self):
        self.config = self._read_config()

    def _read_config(self):
        config = {}
        config_path = args_dict['config_path']
        with open(config_path,'r') as f:
            for line in f.readlines():
                try:
                    config[line.split('=')[0].strip()] = line.split('=')[1].strip()
                except:
                    print("Config parameter error")
        return config

class UserData(object):
    def __init__(self):
        self.userdata = self._read_users_data()

    def _read_users_data(self):
        userdata = []
        data_path = args_dict['data_path']
        with open(data_path,'r') as f:
            for line in f.readlines():
                t = (line.split(',')[0].strip(),line.split(',')[1].strip())
                userdata.append(t)
            return userdata

def cal_salary(nid,salary):
    salary = int(salary)
    salary_list = [nid,salary]
    p = 0.00
    insure = 0.00
    min_s = float(config_dict['JiShuL'])
    max_s = float(config_dict['JiShuH'])
    for key,value in config_dict.items():
        if key == 'JiShuL' or key == 'JiShuH':
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
    elif s1 > 1500 and s1 <= 4500:
        ratio = 0.10
        extra = 105
    elif s1 > 4500 and s1 <= 9000:
        ratio = 0.20
        extra = 555
    elif s1 > 9000 and s1 <= 35000:
        ratio = 0.25
        extra = 1005
    elif s1 > 35000 and s1 <= 55000:
        ratio = 0.30
        extra = 2755
    elif s1 > 55000 and s1 <= 80000:
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
    return salary_list
    

class IncomTaxCalculator(object):
    def calc_for_all_userdata(self):
        result = []
        for user in user_list:
            result.append(cal_salary(user[0],user[1]))
        return result
        
    def export(self,default='csv'):
        result = self.calc_for_all_userdata()
        with open(args_dict['output_path'],'w') as f:
            writer = csv.writer(f)
            writer.writerows(result)

if __name__ == '__main__':
    print(sys.argv)
    args_dict = Args.get_args(sys.argv)
    c = Config()
    config_dict = c.config
    u = UserData()
    user_list = u.userdata
    c = IncomTaxCalculator()
    c.export()

