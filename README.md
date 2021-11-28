## Patent Project

CLEAR Ventures
Elise Rust & Zachary Poley
November 2021 

Patent parser to download and parse all patent files available at https://bulkdata.uspto.gov/ from years 2010 - 2020.

## Directory:
* Patent_Link_Scraper.py
  * Takes https://bulkdata.uspto.gov/ and generates a table of zip file links containing patents
* Patent_Parser.py
  * Unzipping zip files and generating dictionaries for each patent
* Zip_Download.py
  * Sub script of Patent_Parser.py containing just zip download/unzip process
 * Zip_to_Dict.py
  * Sub script of Patent_Parser.py containing parsing script to generate dictionaries from each patent .html file
 * ZipLinks.csv
  * Table of zip file links containing patents
 * Patents.json
  * Sample dictionaries of first five patents in list
