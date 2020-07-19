# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 17:06:05 2020

@author: kingson
"""

# In[1]: Import stuff
import re
import csv
from bs4 import BeautifulSoup
import requests
import os
from datetime import datetime
import math
from googletrans import Translator


# In[2]: get_soup function
def get_soup(url):
    """
    input url, output a soup object of that url
    """
    page=requests.get(url)
    soup = BeautifulSoup(page.text.encode("utf-8"), 'html.parser')
    return soup

# Test:
# link = 'https://www.indeed.nl/vacatures?q=test+engineer&l=Nederland&sort=date'
# soup = get_soup(link)
# link = soup.find('div', {'class': 'jobsearch-SerpJobCard unifiedRow row result'})
# partial_url = link.a.get('href')
# # This is a partial url, we need to attach the prefix:
# url = 'https://www.indeed.nl'+partial_url
# company = link.find('span',{'class':'company'}).getText()
# date =  link.find('span',{'class':'date'}).getText()
# city = link.find('div', {'class':"accessible-contrast-color-location"}).getText()

# In[3] translate a string from dutch to english
def translate(string):
    translator = Translator()
    result = translator.translate(string, src = 'nl')
    return result.text

# # Test:
# text = """een initiatiefrijke collega die studenten enthousiast kan maken;
# handig en vaardig in een mechanisch-elektrisch lab"""
# test = translate(text)

# # Let me see what if I input english
# test1 = translate(test)
#  #So if input english, the result will still be english, it is fine.
# In[4] Extract information directly from the base url and the job post urls
def extract_page_info(base_url):
    soup = get_soup(base_url)
    basic_info = []
    dateString = datetime.strftime(datetime.now(), '%Y_%m_%d')

    # Loop through all the posting links
    for link in soup.find_all('div', {'class': 'jobsearch-SerpJobCard unifiedRow row result'}):
        
        partial_url = link.a.get('href')
        # This is a partial url, we need to attach the prefix:
        url = 'https://www.indeed.nl'+partial_url

        try: # use try here because sometimes the find function give error
            company = link.find('span', {'class':'company'}).getText()
            company = os.linesep.join([s for s in company.splitlines() if s])
            
        except:
            print("extract from base url failed: {}".format()) # To have an idea how many posts are not extracted
            continue    
        try:
            # Try to go to the single job post links and extract the title and description information
            soup1 = get_soup(url)
            # The job title is held in the h3 tag
            title = soup1.find(name='h3').getText().lower()
            
            description = soup1.find(name='div', attrs={'id': "jobDescriptionText"}).get_text()
            description = os.linesep.join([s for s in description.splitlines() if s])
            description = translate(description) # no matter the text is in nl or en, it will become english with this code
        except:
            print("extract from child url failed: {}/n".format(url))
            continue
        
        basic_info.append([title, company, dateString, url, description])
    return basic_info

# # test:
# link = 'https://www.indeed.nl/vacatures?q=test+engineer&l=Nederland&sort=date'
# test1 = extract_page_info(link)


# In[5] Function to extract data from multiple job posts pages
def get_all_info(query, location, num_pages = 0):
    base_url = 'https://www.indeed.nl/jobs?q={}&l={}&sort=date&fromage=1'.format(query, location)
    # example: https://www.indeed.nl/jobs?q=test&l=Nederland&sort=date&fromage=1
    # with 'fromage=1' here, indeed with search for last 24 hours.
    soup = get_soup(base_url)
        
    # Get the total number of postings found 
    posting_count_string = soup.find(name='div', attrs={'id':"searchCountPages"}).get_text()
    # another way: posting_count_string = posting_count_string[posting_count_string.find('van')+2:].strip()
    
    posting_count_string = (posting_count_string.split()[3]).replace('.','') # make sure 1.230 will be read as 1230
    # print('posting_count_string: {}'.format(posting_count_string))
    # print('type is: {}'.format(type(posting_count_string)))
    posting_count = int(posting_count_string)
    # print(type(posting_count), posting_count)
    
    # Limit nunmber of pages to get
    max_pages = math.ceil(posting_count / 15)
    if num_pages > max_pages or num_pages == 0:
        num_pages = max_pages
        
    # initialize a list to easily save the data
    basic_info = []
    
    for i in range(0, num_pages):
        num = i * 10 # every page has 15 posts, so here is a bug of indeed itself
        base_url = 'https://www.indeed.nl/jobs?q={}&l={}&sort=date&fromage=1&start={}'.format(query, location, num)

        try:
            basic_info_part = extract_page_info(base_url)
            basic_info.extend(basic_info_part)
            
        except:
            print("This page of jobs are not extracted:{}/n".format(base_url))
            continue
    
    return basic_info # a list of lists like this: [title, company, date, url, description]

# Test:
# base_info = get_base_info('test engineer "sensor"', 'Nederland', 2)

# In[6] save the information list to a json file
def save_data(query, abs_path, location = 'Nederland', num_pages = 0):
    basic_info = get_all_info(query, location, num_pages)    
    file_name = abs_path
    with open(file_name, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(basic_info)
# In[] Run !!
query = '(engineer OR scientist OR researcher OR engineering OR technician) AND (master or M.Sc or MSc or PhD) -internship -intern'
path = r'e:/Python3732/Scripts/web_scraping/daily_job_scraping_Kingson.csv' # r here means "raw strings"
save_data(query, path, 'Nederland', 0) 
print("finished extracting jobs for me!")
