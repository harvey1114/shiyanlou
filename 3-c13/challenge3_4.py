import re 
from datetime import datetime

def open_parser(filename):
    with open(filename) as logfile:
        
        pattern = (r''
                   r'(\d+.\d+.\d+.\d+)\s-\s-\s'  
                   r'\[(.+)\]\s' 
                   r'"GET\s(.+)\s\w+/.+"\s'  
                   r'(\d+)\s'  
                   r'(\d+)\s'  
                   r'"(.+)"\s'  
                   r'"(.+)"'
                   )
        parsers = re.findall(pattern, logfile.read())
    return parsers

def main():

    logs = open_parser('/home/shiyanlou/Code/nginx.log')

    ips = {}
    urls = {}
    pattern = re.compile('11/Jan/2017')
    for log in logs:
        if pattern.search(log[1]):    
            if ips.get(log[0],0) == 0:
                ips[log[0]] = 1
            else:
                ips[log[0]] += 1
        if log[3] == '404':
            if urls.get(log[2],0) == 0:
                urls[log[2]] = 1
            else:
                urls[log[2]] += 1
    ip_key = max(ips,key=ips.get)
    ip_dict = {}
    ip_dict[ip_key]=ips[ip_key]
    url_key = max(urls,key=urls.get)
    url_dict = {}
    url_dict[url_key] = urls[url_key]
    return ip_dict, url_dict


if __name__ == '__main__':

    ip_dict, url_dict = main()
    print(ip_dict, url_dict)
