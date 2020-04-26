#!/usr/bin/env python
# coding: utf-8

# In[125]:


#import libraries
import os
import sys
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import urllib.request


# In[126]:


#create an http header to avoid 403 Forbidden http error
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,} 

#url of the data source
page_url = "http://www.worldometers.info/coronavirus/"

#download page html
request=urllib.request.Request(page_url,None,headers) #The assembled request
response = urllib.request.urlopen(request)
page_html = response.read() 


# In[127]:


#create beautifulsoup object for parsing html
soup = BeautifulSoup(page_html, "html.parser")


# In[128]:


#extract table rows

data = [] #list to store records
table = soup.find('table', attrs={"id":"main_table_countries_today"}) #extract main table
table_body = table.find('tbody') #extract table body

rows = table_body.find_all('tr') #extract table tows
for row in rows:  #extract attributes of columns in each row
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols] 
    data.append([ele if ele else None for ele in cols])


# In[130]:


#extract table headers
table_headers = table.find('thead')

t_headers = table_headers.find_all('th')

column_names = [h.get_text() for h in t_headers]


# In[131]:


len(column_names)


# In[132]:


#create pandas dataframe with scrapped data and column headers
df = pd.DataFrame(data, columns = column_names)


# In[133]:


df.head()


# In[134]:


#rename irregular column names
df = df.rename(columns = {"Country,Other":"Country","Tests/\n1M pop\n":"Tests/1M pop"})


# In[135]:


#filter out records of continents
df = df[~(df.Country.isin(np.append(df.Continent.unique(), np.array(["Oceania","World"])))) ].reset_index(drop=True)


# In[136]:


#df.info()


# In[138]:


#storing numerical fields to a list
colsToChange = [col for col in df.columns if col not in ['Country','Continent']]

#removing commas in numbers stored as string before data type conversion
for c in colsToChange:
    df[c] = df[c].str.replace(",","")


# In[147]:


#remove nulls and convert to integer
df['TotalCases'] = df['TotalCases'].fillna(0).astype(np.int64)

df['NewCases'] = df['NewCases'].fillna(0).astype(np.int64)


# In[149]:


#calculate worldwide numbers
world_cases = df.TotalCases.sum()

world_new_cases = df['NewCases'].sum()


# In[151]:


#calculate india numbers
india_total_cases = int(df.loc[df.Country == "India"]['TotalCases'])

india_new_cases = int(df.loc[df.Country == "India"]['NewCases'])

#output
print(world_cases)
print(world_new_cases)
print(india_total_cases)
print(india_new_cases)

