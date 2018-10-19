#!/usr/bin/env python3

import sys

if len(sys.argv) == 2:
    try:
        salary = int(sys.argv[1])
        
    except:
        print("Parameter Error")
        sys.exit(-1)

    if salary >= 3500:
        pure_salary= salary - 3500
    else:
        print("The salary is at least 3500")
        sys.exit(-1)
    ratio,extra = 0.00,0
    if pure_salary <=1500: 
        ratio = 0.03
        extra = 0
    elif pure_salary > 1500 and pure_salary <= 4500:
        ratio = 0.10
        extra = 105
    elif pure_salary > 4500 and pure_salary <= 9000:
        ratio = 0.20
        extra = 555
    elif pure_salary > 9000 and pure_salary <= 35000:
        ratio = 0.25
        extra = 1005
    elif pure_salary > 35000 and pure_salary <= 55000:
        ratio = 0.30
        extra = 2755
    elif pure_salary > 55000 and pure_salary <= 80000:
        ratio = 0.35
        extra = 5505
    else:
        ratio = 0.45
        extra = 13505
    tax = pure_salary * ratio - extra
    print("{:.2f}".format(tax))
else:
    print("Parameter Error")

