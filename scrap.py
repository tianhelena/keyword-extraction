#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 13:50:27 2021

@author: tianzhang
"""

# libraries
import urllib.request
from bs4 import BeautifulSoup
import csv
import requests
import re
from os.path import join


##Web scap all links of from Page 1-15 on IMF blog website
htmls=[]
l = [i for i in range(15)][1:]
ink='https://blogs.imf.org/page/'
for each in l:
    link=ink+str(each)
    req = requests.get(link)
    soup = BeautifulSoup(req.content, 'html.parser')
    for link in soup.find_all('a', 
                              attrs={'href': re.compile("^https://")}):
        # display the actual urls
        a=link.get('href')
        htmls.append(a)

## Select links start with Year 2021        
must='https://blogs.imf.org/2021/'
result = [i for i in htmls if i.startswith(must)]
res = []
for i in result:
    if i not in res:
        res.append(i)
        




# Put your URL here
for url in res: 
# url = 'https://blogs.imf.org/2021/11/24/how-domestic-violence-is-a-threat-to-economic-development/'
#     # Fetching the html
    request = urllib.request.Request(url)
    content = urllib.request.urlopen(request)
    # Parsing the html 
    parse = BeautifulSoup(content, 'html.parser')
    text = parse.find_all(text=True)
    
    
    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        # there may be more elements you don't want, such as "style", etc.
    ]
    
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    
    
    start=output.rfind('Search for: ')+88
    end1=output.find('Related links:')
    if end1>0: 
        end=end1
    else: 
        
        end=output.find('We want to hear from you!')
    
    output=output[start:end]
    
    output.replace('\n',"")
    name=url[33:len(url)-30]+'.txt'
    with open(join('imf-articles', name), 'w') as f:
        f.writelines(output)
    print(url)
        
    






