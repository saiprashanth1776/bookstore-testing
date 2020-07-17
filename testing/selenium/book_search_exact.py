from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
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

def compare(book_name,result):
    res_words=result.split()
    res_words=[str(res_word).lower() for res_word in res_words ]
    count=0
    #check if the words in search query are in the result
    for word in book_name.split(): 
        if word.lower() not in res_words:
            pass
        else:
            count+=1
    
    #account for titles sometimes having #1 or #2 indicating number of book in series but result not having it
    if count<len(book_name.split())-2:
        return ["result does not have book name in it",0]

    return ["result has the book name in it",1]

def test_exact_book(name,driver,url):
    
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

    #wait till first res loads
    myElem=WebDriverWait(driver,120).until(EC.presence_of_element_located((By.TAG_NAME, 'h3')))

    #check first 5 results
    results=driver.find_elements_by_tag_name("h3")
    for result_index in range(5):
        print("result ",result_index+1,": ",end=" ")
        ans=compare(name,results[result_index].text)
        print(ans[0])
        if ans[1]==1:
            break
    
    if ans[1]==0:
        return "top 5 results did not have the book"
    return "book has a match in top 5 results"

def exact_book_searches(driver,url):
    
    exact_names=get_book_names()
    
    #test a random book from db
    start=randint(0,len(exact_names)-1)
    test_name=exact_names[start]
    print(test_exact_book(str(test_name),driver,url))
    time.sleep(3)
    driver.quit()
    return "testing completed"

driver=webdriver.Firefox()
driver.maximize_window()

print(exact_book_searches(driver,"http://localhost:3000"))