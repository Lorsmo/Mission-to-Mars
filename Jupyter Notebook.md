```python
# Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
```


```python
!which chromedriver
```

    /usr/local/bin/chromedriver



```python
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)
```

# Mission to Mars : Scrape

## NASA Mars News


```python
# Create a dictionary to hold everything pulled from all the sites
scraped_data = {}
```


```python
# Site 1
url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
browser.visit(url)

# Create a Beautiful Soup object
html = browser.html
soup = bs(html, 'html.parser')
```


```python
# Get the news title and store it in the dictionnary
news_title = soup.find('div', class_='content_title').text
scraped_data['news_title'] = news_title
print(scraped_data['news_title'])

# Get the news text and store it in the dictionnary
news_p = soup.find('div', class_='article_teaser_body').text
scraped_data['news_p'] = news_p
print(scraped_data['news_p'])
```

    NASA's Curiosity Rover Finds an Ancient Oasis on Mars
    New evidence suggests salty, shallow ponds once dotted a Martian crater — a sign of the planet's drying climate.


## JPL Mars Space Images - Featured Image


```python
# Site 2 : Get the featured image and description
url = 'https://www.jpl.nasa.gov/spaceimages/'
browser.visit(url)
```


```python
# Create a Beautiful Soup object
html = browser.html
soup = bs(html, 'html.parser')
```


```python
# Get the featured image and the description
link_image = soup.find('article')['style'].split("'")[1]
```


```python
url = 'https://www.jpl.nasa.gov'

# Store the image and description in the dictionnary
scraped_data['featured_image_url'] = url + link_image
scraped_data['description'] = soup.find('article')['alt']
print(scraped_data['featured_image_url'])
print(scraped_data['description'])
```

    https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA19036-1920x1200.jpg
    'Confidence Hills' -- The First Mount Sharp Drilling Site


# Mars Weather


```python
# Site 3 - Twitter - Get last weather tweet
url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)
# Grab the last tweet
html = browser.html
soup = bs(html, 'html.parser')
```


```python
# Store the text in the dictionnary
scraped_data['mars_weather'] = soup.find('a', class_="twitter-timeline-link u-hidden").previousSibling
print(scraped_data['mars_weather'])
```

    InSight sol 310 (2019-10-10) low -102.2ºC (-152.0ºF) high -26.6ºC (-15.8ºF)
    winds from the SSE at 5.0 m/s (11.2 mph) gusting to 19.1 m/s (42.8 mph)
    pressure at 7.20 hPa


# Mars Facts


```python
 # Site 4 - Get the table
facts_url = 'https://space-facts.com/mars/'

# use pandas to parse the table
facts_df = pd.read_html(facts_url)[1]
facts_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Equatorial Diameter:</td>
      <td>6,792 km</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Polar Diameter:</td>
      <td>6,752 km</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mass:</td>
      <td>6.39 × 10^23 kg (0.11 Earths)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Moons:</td>
      <td>2 (Phobos &amp; Deimos)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Orbit Distance:</td>
      <td>227,943,824 km (1.38 AU)</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Orbit Period:</td>
      <td>687 days (1.9 years)</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Surface Temperature:</td>
      <td>-87 to -5 °C</td>
    </tr>
    <tr>
      <th>7</th>
      <td>First Record:</td>
      <td>2nd millennium BC</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Recorded By:</td>
      <td>Egyptian astronomers</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Rename columns
facts_df.columns = ['Description', 'Value']

# Set index on 'Description'
facts_df.set_index('Description', inplace=True)
facts_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Value</th>
    </tr>
    <tr>
      <th>Description</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Equatorial Diameter:</th>
      <td>6,792 km</td>
    </tr>
    <tr>
      <th>Polar Diameter:</th>
      <td>6,752 km</td>
    </tr>
    <tr>
      <th>Mass:</th>
      <td>6.39 × 10^23 kg (0.11 Earths)</td>
    </tr>
    <tr>
      <th>Moons:</th>
      <td>2 (Phobos &amp; Deimos)</td>
    </tr>
    <tr>
      <th>Orbit Distance:</th>
      <td>227,943,824 km (1.38 AU)</td>
    </tr>
    <tr>
      <th>Orbit Period:</th>
      <td>687 days (1.9 years)</td>
    </tr>
    <tr>
      <th>Surface Temperature:</th>
      <td>-87 to -5 °C</td>
    </tr>
    <tr>
      <th>First Record:</th>
      <td>2nd millennium BC</td>
    </tr>
    <tr>
      <th>Recorded By:</th>
      <td>Egyptian astronomers</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Convert the table to html
html_table = facts_df.to_html()
html_table
```




    '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>Value</th>\n    </tr>\n    <tr>\n      <th>Description</th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>Equatorial Diameter:</th>\n      <td>6,792 km</td>\n    </tr>\n    <tr>\n      <th>Polar Diameter:</th>\n      <td>6,752 km</td>\n    </tr>\n    <tr>\n      <th>Mass:</th>\n      <td>6.39 × 10^23 kg (0.11 Earths)</td>\n    </tr>\n    <tr>\n      <th>Moons:</th>\n      <td>2 (Phobos &amp; Deimos)</td>\n    </tr>\n    <tr>\n      <th>Orbit Distance:</th>\n      <td>227,943,824 km (1.38 AU)</td>\n    </tr>\n    <tr>\n      <th>Orbit Period:</th>\n      <td>687 days (1.9 years)</td>\n    </tr>\n    <tr>\n      <th>Surface Temperature:</th>\n      <td>-87 to -5 °C</td>\n    </tr>\n    <tr>\n      <th>First Record:</th>\n      <td>2nd millennium BC</td>\n    </tr>\n    <tr>\n      <th>Recorded By:</th>\n      <td>Egyptian astronomers</td>\n    </tr>\n  </tbody>\n</table>'




```python
# Replace automatic strings in order to format the table in index.html
html_table = html_table.replace('\n', '').replace('<th></th>      <th>Value</th>', '<th>Description</th> <th>Value</th>')
html_table = html_table.replace('<th>Description</th>      <th></th>', ' ')
html_table = html_table.replace('<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">', ' ')
scraped_data['table'] = html_table
print(scraped_data['table'])
```

           <th>Description</th> <th>Value</th>    </tr>    <tr>           </tr>  </thead>  <tbody>    <tr>      <th>Equatorial Diameter:</th>      <td>6,792 km</td>    </tr>    <tr>      <th>Polar Diameter:</th>      <td>6,752 km</td>    </tr>    <tr>      <th>Mass:</th>      <td>6.39 × 10^23 kg (0.11 Earths)</td>    </tr>    <tr>      <th>Moons:</th>      <td>2 (Phobos &amp; Deimos)</td>    </tr>    <tr>      <th>Orbit Distance:</th>      <td>227,943,824 km (1.38 AU)</td>    </tr>    <tr>      <th>Orbit Period:</th>      <td>687 days (1.9 years)</td>    </tr>    <tr>      <th>Surface Temperature:</th>      <td>-87 to -5 °C</td>    </tr>    <tr>      <th>First Record:</th>      <td>2nd millennium BC</td>    </tr>    <tr>      <th>Recorded By:</th>      <td>Egyptian astronomers</td>    </tr>  </tbody></table>


# Mars Hemispheres


```python
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
    print(url_hemisphere)
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
```

    https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced
    https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced
    https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced
    https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced



```python
# Store the list of dictionnaries in the main dictionnary
scraped_data['hemispheres'] = hemisphere_image_urls
print(scraped_data['hemispheres'])
```

    [{'title': 'Cerberus Hemisphere Enhanced', 'img_url': 'https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg'}, {'title': 'Schiaparelli Hemisphere Enhanced', 'img_url': 'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg'}, {'title': 'Syrtis Major Hemisphere Enhanced', 'img_url': 'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg'}, {'title': 'Valles Marineris Hemisphere Enhanced', 'img_url': 'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg'}]

