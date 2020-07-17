from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
from random import randint
import pandas as pd

"""!!!!!!!!!!!!!    IMPORTANT: MUST HAVE books.csv IN THE SAME FOLDER AS THIS    !!!!!!!!!!!!!!!!!!!!!!!!!"""
def get_book_names():
    df=pd.read_csv("books.csv")
    return list(df["original_title"])

def login(driver,url):
    driver.get(url)

    myElem=WebDriverWait(driver,120).until(EC.presence_of_element_located((By.TAG_NAME, 'button')))
    login_button=driver.find_element_by_tag_name("button")
    login_button.click()
    
    #email
    myElem=WebDriverWait(driver,120).until(EC.presence_of_element_located((By.ID, 'exampleInputEmail1')))
    email_ele=driver.find_elements_by_id("exampleInputEmail1")
    email_ele=email_ele[0]
    email_ele.send_keys("anish@gmail.com")

    #pwd
    pwd_ele=driver.find_elements_by_id("exampleInputPassword1")
    pwd_ele=pwd_ele[0]
    pwd_ele.send_keys("anish123")

    #submit
    buttons=driver.find_elements_by_tag_name("button")
    submit_button=buttons[1]
    submit_button.click()

def check_dates_descend(dates):
    just_dates=[]
    for date in dates:
        i=0
        for i in range(len(date)):
            if (date[i]=="2" or date[i]=="1") or date[i]=="0":
                break

        just_dates.append(date[i]+date[i+1]+date[i+2]+date[i+3])    
    
    for date_index in range(len(just_dates)-1):
            d1=int(just_dates[date_index])
            d2=int(just_dates[date_index+1])
            if d1<d2:
                return 0
    return 1
    
def order_check(name,driver,url):
    login(driver,url)
    
    #click on books search button
    myElem=WebDriverWait(driver,120).until(EC.presence_of_element_located((By.CLASS_NAME, 'navbar-brand')))
    tags=driver.find_elements_by_tag_name("a")
    tags[1].click()

    #enter name
    rec_input=driver.find_element_by_tag_name("input")
    rec_input.send_keys(name)

    #submit for search
    submit=driver.find_element_by_tag_name("button")
    submit.click()

    #change select to oldest
    select = Select(driver.find_element_by_tag_name('select'))
    select.select_by_value('Oldest')
    select.select_by_value('Newest')

    #wait till first res loads
    myElem=WebDriverWait(driver,120).until(EC.presence_of_element_located((By.TAG_NAME, 'h3')))

    #get dates
    results=driver.find_elements_by_tag_name("h5")
    dates=[result.text for result in results]
    ans=check_dates_descend(dates)

    if ans==1:
        return "it is sorted in descending order"
    
    return "it is not sorted correctly"

def test_descending_order(driver,url):
    exact_names=get_book_names()
    
    #test a random book from db
    start=randint(0,len(exact_names)-1)
    test_name=exact_names[start]
    print(order_check(str(test_name),driver,url))
    time.sleep(3)
    driver.quit()
    return "testing completed"


driver=webdriver.Firefox()
driver.maximize_window()

print(test_descending_order(driver,"http://localhost:3000"))