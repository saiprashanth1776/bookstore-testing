from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from random import randint
import pandas as pd

"""!!!!!!!!!!!!!    IMPORTANT: MUST HAVE books.csv IN THE SAME FOLDER AS THIS    !!!!!!!!!!!!!!!!!!!!!!!!!"""

def get_book_names():
    df=pd.read_csv("books.csv")
    return list(df["original_title"])
        
def login(driver,url):
    driver.get(url)
    login_button=driver.find_element_by_tag_name("button")
    login_button.click()
    
    #email
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

def check_reccomendation(driver,url):
    
    #driver=webdriver.Firefox()
    login(driver,url)

    #wait till page loads then click on recommendations    
    myElem=WebDriverWait(driver,120).until(EC.presence_of_element_located((By.CLASS_NAME, 'navbar-brand')))
    tags=driver.find_elements_by_tag_name("a")
    tags[0].click()
    
    #input some book name that exists in db
    book_names=get_book_names()
    book_name=book_names[randint(0,len(book_names)-1)]
    print("book name used is ",book_name)
    rec_input=driver.find_element_by_tag_name("input")
    rec_input.send_keys(str(book_name))

    #submit
    submit=driver.find_element_by_tag_name("button")
    submit.click()

    #check results
    recommendations=tags=driver.find_elements_by_tag_name("a")
    
    try:
        recommendations=recommendations[-5:]
    except:
        driver.quit()
        return "5 recommmendations were not returned"
    
    recommendationURLs=[recommendation.get_attribute("href") for recommendation in recommendations]
    
    
    for recommendation_index in range(len(recommendationURLs)):
        print("recommendation number ",recommendation_index+1," : ",end="")
        
        try:
            driver.get(recommendationURLs[recommendation_index])
            print("valid link")

        except:
            print("invalid link")

    driver.quit()
    return "reccomendations successfully tested"

driver=webdriver.Firefox()
driver.maximize_window()
print(check_reccomendation(driver,"http://localhost:3000"))