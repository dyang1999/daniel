#!/usr/bin/env python
# coding: utf-8

# In[1]:


import urllib.request,sys,time
from bs4 import BeautifulSoup
import requests
import pandas as pd


# In[10]:


pagesToGet= 1

upperframe=[]  
for page in range(1,pagesToGet+1):
    print('processing page :', page)
    url = 'https://www.aljazeera.com/search/earthquakes?page='+str(page)
    print(url)
    
    #an exception might be thrown, so the code should be in a try-except block
    try:
        #use the browser to get the url. This is suspicious command that might blow up.
        page=requests.get(url)                             # this might throw an exception if something goes wrong.
    
    except Exception as e:                                   # this describes what to do if an exception is thrown
        error_type, error_obj, error_info = sys.exc_info()      # get the exception information
        print ('ERROR FOR LINK:',url)                          #print the link that cause the problem
        print (error_type, 'Line:', error_info.tb_lineno)     #print error info and line that threw the exception
        continue                                              #ignore this page. Abandon this and go back.
    time.sleep(2)   
    soup=BeautifulSoup(page.text,'html.parser')
    frame=[]
    links=soup.find_all('article',attrs={'class':'gc gc--type-customsearch#result gc--list gc--with-image'})
    print(len(links))
    
    Links = []
    
    for j in links:
        x = j.find('a')['href'].strip()
        print (x)
        Links.append(x)
        
    for url in Links:

        # Make a GET request to fetch the raw HTML content
        html_content = requests.get(url).text

        # Parse the html content
        soup = BeautifulSoup(html_content, 'html.parser')

        #print(soup)

        title = soup.find_all('h1')[0].get_text()
        print('\033[1m' + title + '\033[0m' + '\n')

        text = soup.find('div', class_ = 'wysiwyg wysiwyg--all-content css-az20b6')
        body = ''
        try:
            for para in text.find_all("p"):
                body += para.get_text() + '\n'
            print(body)
            body = title + '\n' + body + '\n' + url

            with open('./Articles/' + title, 'w+') as f:
                # write text to local file as .txt
                f.write(body)
                f.close()
                
        except AttributeError:
            continue


# In[ ]:




