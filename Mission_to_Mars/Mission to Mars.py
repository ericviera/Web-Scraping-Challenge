#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependancies
import os
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd


# In[2]:


# Make sure latest version of chromedriver is installed on machine
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# ## NASA Mars News

# In[3]:


url = "https://mars.nasa.gov/news/"
browser.visit(url)


# In[4]:


html = browser.html
soup = bs(html, 'html.parser')

news_title = soup.find('div', class_='list_text').find('a').text
news_p = soup.find('div', class_='article_teaser_body').text


print(news_title)
print(news_p)


# ## JPL Mars Space Images - Featured Image

# In[5]:


featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(featured_image_url)


# In[8]:


html_image = browser.html
soup = bs(html_image, "html.parser")

image_url = soup.find('article')['style']
image_url


# In[12]:


url = 'https://www.jpl.nasa.gov'
image_url = soup.find('article')['style'].replace(
    'background-image: url(', '').replace(');', '')[1:-1]

image_url = url+image_url
image_url


# ## Mars Facts
#

# In[13]:


mars_facts = 'https://space-facts.com/mars/'
browser.visit(mars_facts)


# In[14]:


tables = pd.read_html(mars_facts)
tables


# In[17]:


df = tables[0]
df.columns = ['Description', 'Value']
df


# In[18]:


html_table = df.to_html()
html_table


# In[19]:


html_table.replace('\n', '')


# In[20]:


df.to_html('table.html')


# ## Mars Hemispheres

# In[30]:


hemisphere = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemisphere)


# In[29]:


html_hemispheres = browser.html
soup = bs(html_hemispheres, 'html.parser')

images = soup.find_all('div', class_='item')

hemisphere_image_urls = []

main_url = 'https://astrogeology.usgs.gov'

for item in images:
    title = item.find('h3').text
    img_search_url = item.find('a', class_='itemLink product-item')['href']
    browser.visit(main_url + img_search_url)
    img_search_url = browser.html
    soup = bs(img_search_url, 'html.parser')
    img_url = main_url + soup.find('img', class_='wide-image')['src']
    hemisphere_image_urls.append({"title": title, "img_url": img_url})

hemisphere_image_urls


# In[ ]:
