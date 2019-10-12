#!/usr/bin/env python
# coding: utf-8

# Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time

# Create function to open the browser
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

# Create a dictionary to hold everything pulled from all the sites
scraped_data = {}

# Create function 'scrape' to pull datas
def scrape():
    browser = init_browser()

    # Site 1
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    # Create a Beautiful Soup object
    html = browser.html
    soup = bs(html, 'html.parser')

    # Get the news title and store it in the dictionnary
    news_title = soup.find('div', class_='content_title').text
    scraped_data['news_title'] = news_title

    # Get the news text and store it in the dictionnary
    news_p = soup.find('div', class_='article_teaser_body').text
    scraped_data['news_p'] = news_p

    # Site 2 : Get the featured image and description
    url = 'https://www.jpl.nasa.gov/spaceimages/'
    browser.visit(url)

    # Create a Beautiful Soup object
    html = browser.html
    soup = bs(html, 'html.parser')

    # Get the featured image and the description
    results = soup.find('article')['style']
    scraped_data['description'] = soup.find('article')['alt']

    relative_image_path = (results.split("'"))[1]

    url = 'https://www.jpl.nasa.gov'
    featured_image_url = url + relative_image_path

    # Store the image in the dictionnary
    scraped_data['featured_image_url'] = featured_image_url

    # Site 3 - Twitter - Get last weather tweet
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # Grab the last tweet
    html = browser.html
    soup = bs(html, 'html.parser')

    # Store the text in the dictionnary
    scraped_data['mars_weather'] = soup.find('a', class_= "twitter-timeline-link u-hidden").previousSibling

    # Site 4 - Get the table
    facts_url = 'https://space-facts.com/mars/'

    # use pandas to parse the table
    facts_df = pd.read_html(facts_url)[1]

    # Rename columns
    facts_df.columns = ['Description', 'Value']

    # Set index on 'Description'
    facts_df.set_index('Description', inplace=True)

    # Convert the table to html
    html_table = facts_df.to_html()

    # Replace automatic strings in order to format the table in index.html
    html_table = html_table.replace('\n', '').replace('<th></th>      <th>Value</th>', '<th>Description</th> <th>Value</th>')
    html_table = html_table.replace('<th>Description</th>      <th></th>', ' ')
    html_table = html_table.replace('<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">', ' ')
    
    # Store the table in the dictionnary
    scraped_data['table'] = html_table

    # Site 5 -
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # grab the links for the hemispheres
    html = browser.html
    soup = bs(html, 'html.parser')
    soup_links = soup.find_all('div', class_="description")

    # Create an empty list to store the dictionnaries with 'title' and 'img_url'
    hemisphere_image_urls = []

    # Create an empty dictionnary to store 'title' and 'img_url'
    dict_hemi = {}

    # Loop through the four links
    for link in soup_links:
        url_hemisphere = 'https://astrogeology.usgs.gov' + link.find('a')['href']

        # Open the browser for each link
        browser.visit(url_hemisphere)

        # Let 1sec after opening the new page
        time.sleep(1)

        html = browser.html
        soup = bs(html, 'html.parser')
        title = soup.find('h2', class_='title').text
        img_url = soup.find('img', class_='wide-image')['src']
        dict_hemi["title"]= title
        dict_hemi["img_url"]= 'https://astrogeology.usgs.gov' + img_url
        hemisphere_image_urls.append(dict_hemi.copy())

    # Store the list of dictionnaries in the main dictionnary
    scraped_data['hemispheres'] = hemisphere_image_urls

    # Close the browser after scraping
    browser.quit()

    # Return results
    return scraped_data
