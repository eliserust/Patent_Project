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
      zip_file_links.append(os.path.join(temp_url, link.get('href'))) # add links to zip_file_links list


print(zip_file_links)
 
# filter for .zip urls
zip_file_links = [k for k in zip_file_links if 'zip' in k]

###### Clean up Zip_File_Links list
zip_file_links = [k for k in zip_file_links if 'zip' in k] # remove non-zip links
zip_file_links = [k for k in zip_file_links if 'http' in k] # remove short links

zip_df = pd.DataFrame(zip_file_links) # convert to dataframe

# Write dataframe of links to .csv
zip_df.to_csv("/Users/eliserust/Desktop/ZipLinks.csv")
