from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from random import randint

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

def check_reccomendation_invalid_ip(driver,url):
    
    #driver=webdriver.Firefox()
    login(driver,url)

    #wait till page loads then click on recommendations    
    myElem=WebDriverWait(driver,120).until(EC.presence_of_element_located((By.CLASS_NAME, 'navbar-brand')))
    tags=driver.find_elements_by_tag_name("a")
    tags[0].click()
    
    #trash input
    junk_names=["asdasd","hdfgfdf","dsewa","sdsgwa","moams"]
    junk_name=junk_names[randint(0,4)]
    rec_input=driver.find_element_by_tag_name("input")
    rec_input.send_keys(junk_name)

    time.sleep(3)
    #submit
    submit=driver.find_element_by_tag_name("button")
    submit.click()

    time.sleep(3)
    #check if right error message is generated
    ele=driver.find_element_by_tag_name("input")
    if ele.get_attribute("value")=="We did not find this title. Please try again!":
        driver.quit()
        return "properly handled input with no matches"
    else:
        driver.quit()
        return "returned value even for junk string"


driver=webdriver.Firefox()
driver.maximize_window()
print(check_reccomendation_invalid_ip(driver,"http://localhost:3000"))