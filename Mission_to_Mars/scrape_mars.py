# Dependancies
import os
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    # Initialize browser
    browser = init_browser()

    # ---------------------------------------------------------------------------------------------------------------
    # Visit Featured News 'https://mars.nasa.gov/news/'
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')
    # Get the Article Title
    news_title = soup.find('div', class_='list_text').find('a').text
    news_title
    # Get the Article Teaser
    news_p = soup.find('div', class_='article_teaser_body').text
    news_p
    # ----------------------------------------------------------------------------------------------------------------
    # Visit Featured Image 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_image_url)
    time.sleep(2)
    # Scrape page into Soup
    html_image = browser.html
    soup = bs(html_image, "html.parser")
    # Get image
    image_url = soup.find('article')['style']
    image_url
    url2 = 'https://www.jpl.nasa.gov'
    image_url = soup.find('article')['style'].replace(
        'background-image: url(', '').replace(');', '')[1:-1]
    image_url = url2+image_url
    image_url
    # ---------------------------------------------------------------------------------------------------------------
    # Visit Mars Facts 'https://space-facts.com/mars/'
    mars_facts = 'https://space-facts.com/mars/'
    browser.visit(mars_facts)
    time.sleep(2)
    tables = pd.read_html(mars_facts)
    tables
    df = tables[0]
    df.columns = ['Description', 'Value']
    df
    html_table = df.to_html()
    html_table
    html_table.replace('\n', '')
    df.to_html('table.html')
    # ----------------------------------------------------------------------------------------------------------------
    # Visit Hemisphere webpage 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemisphere = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere)
    time.sleep(2)
    # Scrape page into Soup
    html_hemispheres = browser.html
    soup = bs(html_hemispheres, 'html.parser')
    items = soup.find_all('div', class_='item')
    hemisphere_image_urls = []
    main_url = 'https://astrogeology.usgs.gov'
    for item in items:
        title = item.find('h3').text
        img_search_url = item.find('a', class_='itemLink product-item')['href']
        browser.visit(main_url + img_search_url)
        img_search_url = browser.html
        soup = bs(img_search_url, 'html.parser')
        img_url = main_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"title": title, "img_url": img_url})
    hemisphere_image_urls
    # ------------------------------------------------------------------------------------------------------

    # Create dictionary

    mars_news = {
        'news_title': news_title,
        'news_p': news_p,
        'image_url': image_url,
        'tables': df,
        'hemisphere_image_urls': hemisphere_image_urls
    }

    # close browser after scraping
    browser.quit()
    # return results
    return mars_news
