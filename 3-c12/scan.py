import sys
import re
import socket
from getopt import getopt

def parserargs():
    shortargs = 'h'
    longargs = ['host=','port=']
    arg_dict={}
    try:
        opts,_ = getopt(sys.argv[1:],shortargs,longargs)
    except:
        print("Parameter Error1")
        sys.exit(-1)
    if len(opts) != 2:
        print("Parameter Error2")
        sys.exit(-1)
    else:
        for arg,value in opts:
            arg_dict[arg] = value
        pattern = re.compile('^(\d+\.){3}(\d+){1}$')
        if not pattern.fullmatch(arg_dict['--host']):
            print('Parameter Error3')
            sys.exit(-1)
        if '-' in str(arg_dict['--port']):
            ports = str(arg_dict['--port']).split('-')
            if len(ports) != 2 or not ports[0].isdigit() or not ports[1].isdigit():
                print('Parameter Error4')
                sys.exit(-1)
        else:
            if not str(arg_dict['--port']).isdigit():
                print('Parameter Error5')
                sys.exit(-1)
    return arg_dict

def scan(ip,ports):
    if '-' in ports:
        startport = int(ports.split('-')[0])
        endport = int(ports.split('-')[1])
        for port in range(startport,endport+1):     
            try:
                s = socket.socket()
                s.settimeout(0.1)
                s.connect((ip,port))
                print('{} open'.format(port))
            except:
                print('{} closed'.format(port))
    else:
        try:
            port = ports
            s = socket.socket()
            s.settimeout(0.1)
            s.connect((ip,port))
            print('{} open'.format(port)) 
        except:
            print('{} closed'.format(port))


if __name__ == '__main__':
    arg_dict =parserargs()
    ports = arg_dict['--port']
    ip = arg_dict['--host']
    scan(ip,ports)
