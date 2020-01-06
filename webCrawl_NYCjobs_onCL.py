#!/usr/bin/env python
# coding: utf-8

# # This is a webCrawl project
# # Gathering craigsList Tech Employement Data.

# In[ ]:


from bs4 import BeautifulSoup
import requests 
import pandas as pd


# In[40]:


url = "https://newyork.craigslist.org/search/npo"


# In[41]:


npo_jobs = {}
job_no = 0
while True:
    
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data,'html.parser')
    jobs = soup.find_all('p',{'class':'result-info'})
    
    for job in jobs:
        
        title = job.find('a',{'class':'result-title'}).text
        location_tag = job.find('span',{'class':'result-hood'})
        location = location_tag.text[2:-1] if location_tag else "N/A"
        date = job.find('time', {'class': 'result-date'}).text
        link = job.find('a', {'class': 'result-title'}).get('href')
        
        job_response = requests.get(link)
        job_data = job_response.text
        job_soup = BeautifulSoup(job_data, 'html.parser')
        job_description = job_soup.find('section',{'id':'postingbody'}).text
        job_attributes_tag = job_soup.find('p',{'class':'attrgroup'})
        job_attributes = job_attributes_tag.text if job_attributes_tag else "N/A"
        
        job_no+=1
        npo_jobs[job_no] = [title, location, date, link, job_attributes, job_description]
        
        
#       print('Job Title:', title, '\nLocation:', location, '\nDate:', date, '\nLink:', link,"\n", job_attributes, '\nJob Description:', job_description,'\n---')
        
    url_tag = soup.find('a',{'title':'next page'})
    if url_tag.get('href'):
        url= 'https://newyork.craigslist.org' + url_tag.get('href')
        print(url)
    else:
        break
        
print("Total Jobs:", job_no)
npo_jobs_df = pd.DataFrame.from_dict(npo_jobs, orient = 'index', columns = ['Job Title','Location','Date', 'Link', 'Job Attributes', 'Job Description'])


# In[42]:


npo_jobs_df.head()


# In[43]:


npo_jobs_df.to_csv('npo_jobs.csv')

