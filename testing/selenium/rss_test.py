from selenium import webdriver
import time
import calendar
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def check_rss_url(url): #checks if the url is valid and if date of publication of article is fairly recent  
    
    #initializing web driver
    driver=webdriver.Firefox()
    driver.maximize_window()
    
    #opening url
    try:
        driver.get(url)
    except:
        driver.quit()
        return "error in loading URL, please check link"
    
    #get element that has the date
    try:
        ele=driver.find_elements_by_id("hubspot-author_data")
        ele=ele[0]

    except:
        driver.quit()
        return "page not found in the server of website"

    string=ele.text
    months=(list(calendar.month_name))[1:]
    months=[month[:3] for month in months]

    #extract date from string
    string=string.split()

    for word_index in range(len(string)):
        if string[word_index] in months:
            break
    
    #time of publication
    month=string[word_index]
    month=str((months.index(month))+1)
    day=string[word_index+1]
    day=day[:-1]
    year=string[word_index+2]
    year=year[:-1]

    #current time
    curr_dt=datetime.now()
    curr_day=str(curr_dt.day)
    curr_month=str(curr_dt.month)
    curr_year=str(curr_dt.year)
            
    
    date_format = "%d/%m/%Y"
    a = datetime.strptime(day+'/'+month+'/'+year, date_format) 
    b = datetime.strptime(curr_day+'/'+curr_month+'/'+curr_year, date_format)

    #get difference in days, if its too high, return appropriate message
    delta = b - a
    if delta.days>45:
        driver.quit()
        return "might want to check RSS code or the website, the article is "+str(delta.days)+" days old, which is too long"

    driver.quit()
    return "article is "+str(delta.days)+" days old, which is fine"

def get_rss_urls(url): #gets all the links to articles from rss page
    driver=webdriver.Firefox()
    driver.maximize_window()

    try:
        driver.get(url)
    except:
        print("main RSS page itself doesn't load in time")

    myElem = WebDriverWait(driver,120).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
    tags=driver.find_elements_by_tag_name("a")
    links=[tag.get_attribute("href") for tag in tags]
    driver.quit()
    
    return links

def check_rss(url):
    links=get_rss_urls(url)
    for link_index in range(len(links)-7): #FOR TESTING JUST SHOWING TESTING OF FIRST FIVE URLS
        print("for link ",link_index+1,": ",end="")
        print(check_rss_url(links[link_index]))

check_rss("http://localhost:3000/")
