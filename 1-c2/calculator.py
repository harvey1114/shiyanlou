import sys

def cal_salary(salary):
    expense = salary*0.165
    s1 = salary - expense - 3500
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
    final_salary = salary-expense-tax
    return final_salary

if  __name__ == '__main__':
    user={}
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            key = arg.split(':')[0]
            try:
                value = int(arg.split(':')[1])
            except:
                print("Parameter Error")
                sys.exit(-1)
            value = cal_salary(value)
            user[key] = value
        for key,value in user.items():
            print("{}:{:.2f}".format(key,value))

