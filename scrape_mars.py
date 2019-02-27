from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd

##https://www.dataquest.io/blog/web-scraping-tutorial-python/

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:/webdrivers/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    # Create a library that holds all the Mars' Data
    browser = init_browser()    
    mars_library = {}

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(1) 

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Extract title text
    news_title = soup.find_all('div', class_='content_title')[0].find('a').text.strip()
 
    # Print all Paragraphs
    news_p = soup.find_all('div', class_="article_teaser_body")[0].text.strip()

    #-----------------------------------------------------------------------------
    mars_library['news_title'] = news_title
    mars_library['news_p'] = news_p
    #-----------------------------------------------------------------------------    

    #Use splinter to navigate the site and find the image url for the current
    #Featured Mars Image and assign the url string to a variable called
    #featured_image_url.

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1) 

    # get soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # find the tag : <img ... >
    partial_link_url = soup.find_all('a', class_ = 'button fancybox')[0].get('data-fancybox-href').strip()

    featured_image_url = 'https://www.jpl.nasa.gov' + partial_link_url

    #-----------------------------------------------------------------------------
    mars_library['featured_image_url'] = featured_image_url
    #-----------------------------------------------------------------------------    

    #Visit the Mars Weather twitter account here and scrape the latest Mars
    # weather tweet from the page. Save the tweet text for the weather report
    #as a variable called mars_weather.

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)

    # get soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find_all('p', class_ ="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text" )[0].get_text()
    mars_weather = mars_weather.split("\n")[0]
    #mars_weather = mars_weather.split("ght ")[1]
    #-----------------------------------------------------------------------------
    mars_library['mars_weather'] = mars_weather
    #-----------------------------------------------------------------------------    

    #Visit the Mars Facts webpage here and use Pandas to scrape the table 
    #containing facts about the planet including Diameter, Mass, etc.

    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(1)
    
    tables = pd.read_html(url)
    
    df = tables[0]
    #Use Pandas to convert the data to a HTML table string.
    df.columns = ['Description', 'Value']
    #Set the index to the Description column
    df.set_index('Description', inplace = True)
    #Generate HTML tables from DataFrames.

    html_table = df.to_html()
    #strip unwanted newlines to clean up the table.
    html_table = html_table.replace('\n', '')
    #-----------------------------------------------------------------------------
    mars_library['mars_facts'] = html_table
    #-----------------------------------------------------------------------------   

    #Visit the USGS Astrogeology site here to obtain high resolution
    #images for each of Mar's hemispheres.
    #You will need to click each of the links to the hemispheres in order
    #to find the image url to the full resolution image.
    #Save both the image url string for the full resolution hemisphere image, 
    #and the Hemisphere title containing the hemisphere name. Use a Python
    #dictionary to store the data using the keys img_url and title.
    #Append the dictionary with the image url string and the hemisphere title
    #to a list. This list will contain one dictionary for each hemisphere.

    #url = https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars

    #Save both the image url string for the full resolution hemisphere image,
    #and the Hemisphere title containing the hemisphere name. Use a Python 
    #dictionary to store the data using the keys img_url and title.

    #executable_path = {"executable_path": "C:\webdrivers\chromedriver"}
    #browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(1)   

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
 
    img_links = soup.find_all('div',class_ = 'description')
    # Iterate over the image links to obtain dictionary of img titles and img urls

    dict = {}
    dict_list =[]

    url_link =[] # initialize the list to empty

    for i in img_links:

        title = i.find('h3').text.strip()
        title = title.replace(' Enhanced', '')

        dict['title'] = title

        url_img_link = i.find('a').attrs['href']
        url_link.append(url_img_link)

        #executable_path = {'executable_path': 'chromedriver.exe'}
        #browser = Browser('chrome', **executable_path, headless=False)
    
        url = 'https://astrogeology.usgs.gov' + url_img_link
    
        browser.visit(url)
        time.sleep(1)
    
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        img_urls = soup.find('div', class_="downloads")
        img_urls = img_urls.find('a')["href"]
    
        dict['img_url'] = img_urls
    
        dict_list.append(dict)
        dict={}


    #-----------------------------------------------------------------------------
    mars_library['mars_img_dict'] = dict_list
    #-----------------------------------------------------------------------------     
    browser.quit()
    # Return Library
    return mars_library
