from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from random import randint
import pandas as pd
import csv
import codecs


def get_book_names():
    df=pd.read_csv("books.csv")
    return list(df["original_title"])

def get_rating_of_book(name):
    ratings=[]

    #this type of encoding was code found on stack overflow for some char encoding error in reading a csv
    with codecs.open("books.csv", encoding = "cp1252", errors ='replace') as csvfile:
        csv_file_reader = csv.DictReader(csvfile)
        for row in csv_file_reader:
            #check if this row is the one corresponding to book name
            if row["original_title"]==name:
                #store rating in list of ratings. reason is that a few books have multiple entries for same book name 
                ratings.append(row["ratings_count"])
    
    #in case same book name has multiple entries,return error message
    if len(ratings)>1:
       return [0,"Book name has multiple matches in the csv with different ratings, so it will not be counted"]

    #if no matches were found (shouldn't happen)
    if len(ratings)==0:
        return [0,"no matches for this book were found"]    
    
    #return the rating
    return [1,ratings[0]]

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

def clean(string): #string has book name and url, this simply returns book name only, cutting out the url
    i=0
    try:
        while 1:
            if (string[i+1]!='h' or string[i+2]!='t') or (string[i+3]!='t' or string[i+4]!='p'):
                i+=1
            else:
                break
        return string[:i]
    
    except:
        return "recommendation result empty or invalid"

def check_reccomendation_ratings(driver,url):
    
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

    #if no matches found
    ele=driver.find_element_by_tag_name("input")
    if ele.get_attribute("value")=="We did not find this title. Please try again!":
        driver.quit()
        return "the book name has no matches"

    #get name of each book in recommendation results
    paras=driver.find_elements_by_tag_name("p")
    print("\n\nnames before cleaning are ",[para.text for para in paras],"\n\n")
    names=[clean(paras[i].text) for i in range(1,6)]
    print("names after cleaning are ",names,"\n\n")
    
    #put the ratings in a list to check for ascending order
    ratings=[]
    for name in names:
        if name!="recommendation result empty or invalid":
            res=get_rating_of_book(name)
            
            if res[0]==0:
                print("cannot get rating of the book ",name," the error is: ",res[1])
            else:
                ratings.append(res[1])
        else:
            print("this recommendation result was either empty or invalid")

    if len(ratings)==0:
        driver.quit()
        return "ratings of none of the results could be found"
    
    if len(ratings)==1:
        driver.quit()
        return "only one book's rating was retreived, so the order doesn't really matter"

    for rating_index in range(len(ratings)-1):
        if ratings[rating_index]<ratings[rating_index+1]:
            driver.quit()
            return "results are in the wrong order"
    
    driver.quit()
    return "results are in the right order"
    
driver=webdriver.Firefox()
driver.maximize_window()
print(check_reccomendation_ratings(driver,"http://localhost:3000"))