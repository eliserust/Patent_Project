#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 15:14:09 2021

@author: eliserust
"""

# Goal: From links, read in


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


# Load in dataset of links
path="/Users/eliserust/Desktop/"
filename = "ZipLinks.csv"

zip_links = pd.read_csv(path+filename)
print(zip_links)

# Subset zip_links to just look at first file for testing
zip_1 = zip_links.head(5) # Get first five patent sets
zip_1 = zip_1['0'].to_frame()
zip_1 = zip_1.rename(columns={"0": "Patent Links"}) # rename column



####### Unzip entire .zip file to disk/server
for index, row in zip_1.iterrows():
    
    temp_link = (row[0]) # Set link to be unzipped to row i's link
    #temp_link = str(temp_link)
   # print(temp_link)
    

    with urlopen(temp_link) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall('/tmp/patents_main')
    
     
    
####### Change directory to patents_main folder just created
os.chdir('/tmp/patents_main')
os.listdir() # list all file names in directory
#### Note: Remove .DS_Store file via Terminal


####### Use glob to extract all .html files from html folder
#for filename in glob.glob("*.html"):
#    print(filename)

# Navigate to 'html' subfolders; open .html files in html folder
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
                             

                
print(html_list)

# Write to .csv to check for success
html_df = pd.DataFrame(html_list) # convert to dataframe
html_df.to_csv("/Users/eliserust/Desktop/HTML.csv")


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
