#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import datetime as dt

executable_path = {'executable_path':r'\Users\520 JUJU\Desktop\Python Boot Camp\mission_to_mars\chromedriver.exe'}
def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser('chrome',**executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
# Run all scraping functions and store results in dictionary
    data ={
    "news_title":news_title,
    "news_paragraph": news_paragraph,
    "feature_image": featured_image(browser),
    "facts": mars_facts(),
    "last_modified": dt.datetime.now(),
    "mars_hep": mars_hem(browser)
    }
    return data
def mars_news(browser):

    #Visit the mars nasa news site  
    url= 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional dely for loading the page
    browser.is_element_present_by_css('ul.item_list li.slide',wait_time = 1)

    # Convert the browser html to a soup object and then quite the browser:
    html = browser.html
    news_soup = BeautifulSoup(html,'html.parser')

    #Add try/except for error hanling
    try:
        slide_elem = news_soup.select_one ('ul.item_list li.slide')
        slide_elem.find('div',class_='content_title')


    # Use the parent elecment to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()

    # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
       return None,None
    return news_title,news_p   
def featured_image(browser):

# visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

# Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

# Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time = 1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

# Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    try:
    # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get('src')

    except AttributeError as e:
        print(e)
        return None 
# Use the base URL to create an absolute URL 
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    return img_url
import pandas as pd

def mars_facts():
    #Add try/except for error handling
    try:
        #convert the Mars Facts table to a Panadas DataFrame
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    #Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def mars_hem(browser):
     # Visit the Mars Facts webpage
    # Visit the USGS Astrogeology site
    mh_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
     
    browser.visit(mh_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    main_url = soup.find_all('div', class_='item')
        
    hemisphere_img_urls=[]      
    for x in main_url:
        title = x.find('h3').text
        mh_url = x.find('a')['href']
        hem_img_url= mh_url
            #print(hem_img_url)
        browser.visit(hem_img_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hemisphere_img_original= soup.find('div',class_='downloads')
        hemisphere_img_url=hemisphere_img_original.find('a')['href']
            
        print(hemisphere_img_url)
        img_data=dict({'title':title, 'img_url':hemisphere_img_url})
        hemisphere_img_urls.append(img_data)
        hemisphere_img_urls=['hemisphere_img_urls']
        return hemisphere_img_urls

if __name__ =='__main__':
    #if running as script,print scraped data
    print(scrape_all())
