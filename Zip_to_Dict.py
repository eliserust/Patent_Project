#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 18:12:11 2021

@author: eliserust
"""

# Scrape information of interest from each patent .html page at https://bulkdata.uspto.gov/

## Load in necessary libraries
import requests
import re
import os
import pandas as pd
from zipfile import ZipFile
from io import BytesIO
from urllib.request import urlopen
import glob
import codecs
from bs4 import BeautifulSoup
import pprint
import json
from datetime import datetime


## Navigate to 'html' subfolders; open .html files in html folder
# .tmp folder previously created via zip download process. See Zip_Download.py
# Remove .DS_Store from /tmp/patents_main

rootdir = '/tmp/patents_main'
html_list = [] # empty list for html links

for file in os.listdir(rootdir):
    temp_directory = (os.path.join(rootdir, file)) + "/OG/html"
    #print(temp_directory)
    os.chdir(temp_directory)
    
    for root, dirs, files in os.walk(temp_directory):
        # select file name
        for file in files:
            # check the extension of files
            if file.endswith('.html'):
                # print whole path of files
                #print(os.path.join(root, file))
                html_list.append(os.path.join(root, file))
                             

                
print(html_list) # List of all .html directories in folder


# Write list to json file for future access
with open("html_list.json", "w") as write_file:
    json.dump(html_list, write_file)


# Test on 5 html documents
html_list_test = html_list[:5]


####### Open each .html file
for link in html_list_test:
    
    page = codecs.open(link, "r", "utf-8")
    page_content = page.read()
    
    # Extract table
    soup = BeautifulSoup(page_content, 'lxml')
    table = soup.find_all('td', attrs={"class":"table_data"}) # grab all elements of class "table_data"
    #pprint.pprint(table) # pretty print table
    
    
    # Extract nodes of interest (author, company, patent name, date of publication) from table
    patent_name = table[1].text # Patent Name
    patent_no = table[0].text # Patent Number
    author = table[2].text # Patent Author
    #author = str(soup.find_all(text = re.compile('Filed by'))) # Patent Author
    company = str(soup.find_all(text = re.compile('Assigned to'))) # Patent Company
    date = str(soup.find_all(text = re.compile('Filed on'))) # Date
    
    ## Clean up the dictionary valules
    patent_no = patent_no[3:]  # Remove "US" from front
    patent_no = patent_no[:-3] # Remove "B2" from end
    # print(patent_no)
    
    author = author.strip("[]") # Remove brackets
    author = author.strip("''") # Remove quotes
    author = author.strip("Filed by ")
    # print(author)
    
    company = company.strip("[]") # Remove brackets
    company = company.strip("'") # Remove quotes
    company = company[13:] # Remove "Assigned to" without compromising company name
    # print(company)
    
    date = date[11:]
    sep = ', as'
    date = date.split(sep, 1)[0]
    # print(date)
    
    # Combine into a list
    dict_values = [patent_name, patent_no, author, company, date]
    #print(dict_values)
     
     
    # Create dictionary for individual patent
    dict_keys = ["Patent Name", "Patent Number", "Author(s)", "Company", "Date"]
    zip_dict = zip(dict_keys, dict_values)
    patent_dict = dict(zip_dict)
    
    print(patent_dict)
    
         
    # Write dictinoary to file as JSON
    os.chdir('/Users/eliserust/Desktop')
    with open("Patents.json", "a") as outfile:
	# write a JSON formatted dict obj as string out outfile
        outfile.write(f"{json.dumps(patent_dict)}\n")