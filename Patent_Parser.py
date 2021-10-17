#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 12:24:04 2021

@author: eliserust
"""

# Goal: scrape all the patents that are listed on this page: https://bulkdata.uspto.gov/


## Load in necessary libraries
from bs4 import BeautifulSoup
import requests
import re
from requests_html import HTMLSession
from requests_html import HTML
from lxml import html



##### Create list of links to each year's Patent Official Gazettes
URL = "https://bulkdata.uspto.gov/"

main = requests.get(URL)
soup = BeautifulSoup(main.text)

links = soup.find_all('a')

main_links = []
for link in links:
    print(link.get('href'))
    main_links.append(link.get('href')) # add links to main_links list
    

###### Clean list; remove extraneous links
main_clean = []

for i in main_links:
    #print(type(i))
    patent_url = str(i)

    if 'gazette' in patent_url:
        main_clean.append(patent_url)

print(main_clean) # list of 20 links --> all the gazette URLs



##### Create list of zip file links under each year's Patent Official Gazettes
zip_file_links = []

for link in main_clean: 
    temp_url = link# establish URL as new baseURL
    #print(temp_url)
    html = requests.get(temp_url)
    soup = BeautifulSoup(html.text)
    
    links = soup.find_all('a')
    
    for link in links:
     # print(link.get('href'))
      zip_file_links.append(link.get('href')) # add links to zip_file_links list


print(zip_file_links)
    


