# import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from selenium import webdriver

# splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

# scrape function
def scrape():
    browser = init_browser()

    # visit Mars News Site
    url = "https://redplanetscience.com/"
    
    browser.visit(url)
    # html created
    html = browser.html
    # beautifulsoup object created
    soup = bs(html, "html.parser")
    # beautifulsoup find latest news data
    data = soup.find("div", id="news")
    # use bs to get news title and paragraph info
    news_title = data.find("div", class_="content_title").text
    news_content = data.find("div", class_="article_teaser_body").text
    
    # visit JPL Mars Space Images
    img_url = 'https://spaceimages-mars.com/'
    browser.visit(img_url)
    # create soup object to parse html
    html_img = browser.html
    soup = bs(html_img, "html.parser")
    rel_image = soup.find("img", class_="headerimage fade-in")["src"]
    featured_image_url = img_url + rel_image

    # visit Mars Facts webpage
    facts_url = "https://galaxyfacts-mars.com/"
    browser.visit(url)
    # Use panda's `read_html` to parse the url
    facts_table = pd.read_html(facts_url)

    # convert table to pandas dataframe
    facts_df = facts_table[1]
    facts_df.columns=['Description','Value']
    print(facts_df)

    # convert to html
    facts_html = facts_df.to_html()

    # visit the astrogeology site
    hemis_url = "https://marshemispheres.com/"
    browser.visit(hemis_url)

    # beautiful soup
    html_hemis = browser.html
    hemis_soup = bs(html_hemis, "html.parser")
    hemis_info = hemis_soup.find_all('div', class_='item')

    hemis_list = []
    for item in hemis_info:
        title = item.find('h3').text
        browser.find_by_text(title).first.click()
        html = browser.html
        soup = bs(html, 'html.parser')
        url_ext = soup.find('div', class_='downloads').ul.li.a['href']
        img_url = hemis_url + url_ext
        hemis_dict = {'Title:':title,'IMG URL':img_url}
        hemis_list.append(hemis_dict)
    mars_data = {
        "News Title":news_title,
        "Content":news_content,
        "Featured IMG":featured_image_url,
        "Facts":facts_html,
        "Hemispheres:":hemis_list
    }
    return mars_data