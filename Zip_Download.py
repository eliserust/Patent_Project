#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 18:11:56 2021

@author: eliserust
"""

# Download all zip files to server

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
    
     

    