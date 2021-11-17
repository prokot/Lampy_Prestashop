# coding=utf8
import os
import random
import string
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from selenium.common.exceptions import NoSuchElementException 

driver = webdriver.Chrome(r'/home/lulian/Documents/Lampy_PrestaShop/scripts/ImportSeleniumScript/seleniumdriver/linux/chromedriver')
driver.maximize_window()

def add_items_to_cart(category_url, count):

    page = 1
    added = 0
    i=0
    while True:

        if page == 1:
            driver.get(category_url)
        else:
            driver.get(category_url+"?page="+str(page))

        page_has_loaded()

        product = driver.find_elements(By.CSS_SELECTOR,".product-title > a")[i%12]
        driver.get(product.get_attribute("href"))
        try:
   
            quantity = driver.find_elements(By.CSS_SELECTOR,".product-quantities > span")[0].get_attribute("data-stock")

            no_of_products = random.randint(1,int(quantity))-1

            up_button = driver.find_elements(By.CSS_SELECTOR,".btn.btn-touchspin.js-touchspin.bootstrap-touchspin-up")[0]
            
            for _ in range(0,random.randint(0,min(no_of_products,10))):
                up_button.click()

            driver.find_elements(By.CSS_SELECTOR,".add-to-cart")[0].click()
            added+=1
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "blockcart-modal")))

        except Exception:
            if i%12==0:
                page+=1
        i+=1
        if added==count:
            break



def delete_one_item():
    driver.get("https://localhost/koszyk")

    page_has_loaded()
    time.sleep(0.5)
    elements = driver.find_elements(By.CSS_SELECTOR,"i.material-icons.float-xs-left")
    elements_count = len(elements)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "i.material-icons.float-xs-left")))

    index = random.randint(0,elements_count-1)
    element = elements[index]

    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)
    element.click()

def create_account():
    driver.get("https://localhost/zam%C3%B3wienie")

    page_has_loaded()

    WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".radio-inline")))

    driver.find_elements(By.CSS_SELECTOR,".radio-inline")[0].click()
    

    letters = string.ascii_letters

    name = driver.find_element(By.XPATH,'//input[@name="firstname"]')
    name.clear()
    name.send_keys((''.join(random.choice(letters) for i in range(random.randint(8,15)))))

    lastname = driver.find_element(By.XPATH,'//input[@name="lastname"]')
    lastname.clear()
    lastname.send_keys((''.join(random.choice(letters) for i in range(random.randint(8,15)))))
    
    email = driver.find_element(By.XPATH,'//input[@name="email"]')
    email.clear()
    email_saved = (''.join(random.choice(letters) for i in range(random.randint(8,15))))
    email_saved += "@gmail.com"
    email.send_keys(email_saved)

    pw = driver.find_element(By.XPATH,'//input[@name="password"]')
    pw.clear()
    pw_saved = (''.join(random.choice(letters) for i in range(random.randint(8,15))))
    pw.send_keys(pw_saved)

    driver.find_element(By.XPATH,'//input[@name="customer_privacy"]').click()
    
    submit_button = driver.find_element(By.XPATH,'//button[@name="continue"]')

    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", submit_button)

    driver.find_element(By.XPATH,'//input[@name="psgdpr"]').click()

    submit_button.click()

    return email_saved,pw_saved


def fill_address():

    WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//input[@name="address1"]')))

    letters = string.ascii_letters

    address = driver.find_element(By.XPATH,'//input[@name="address1"]')
    address.clear()
    address.send_keys((''.join(random.choice(letters) for i in range(random.randint(8,15)))))

    postal = driver.find_element(By.XPATH,'//input[@name="postcode"]')
    postal.clear()
    postal.send_keys('07-410')

    city = driver.find_element(By.XPATH,'//input[@name="city"]')
    city.clear()
    city.send_keys((''.join(random.choice(letters) for i in range(random.randint(8,15)))))


    submit_button = driver.find_element(By.XPATH,'//button[@name="confirm-addresses"]')

    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", submit_button)
    submit_button.click()

def choose_delivery():

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[text()[contains(., "DPD")]]')))
    
    if random.randint(0,1) == 1:
        driver.find_element(By.XPATH,'//*[text()[contains(., "DPD")]]').click()

    submit_button = driver.find_element(By.XPATH,'//button[@name="confirmDeliveryOption"]')

    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", submit_button)
    submit_button.click()

def choose_payment():

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[text()[contains(., "gotówką")]]')))
    
    
    driver.find_element(By.XPATH,'//*[text()[contains(., "gotówką")]]').click()

    driver.find_element(By.XPATH,'//input[@name="conditions_to_approve[terms-and-conditions]"]').click()

    submit_button = driver.find_element(By.XPATH,'//*[text()[contains(., "Złóż zamówienie")]]')
      
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", submit_button)
    submit_button.click()

def check_status():

    driver.get("https://localhost/moje-konto")
    page_has_loaded()

    driver.find_element(By.XPATH,'//*[text()[contains(., "Historia i szczegóły zamówień")]]').click()

    elements = driver.find_elements(By.XPATH,'//*[text()[contains(., "Przygotowanie w toku")]]')

    assert len(elements) > 0
   
def page_has_loaded():
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'

lamps_count = 10

count_from_first_tab = random.randint(1,lamps_count-1)
count_from_second_tab = lamps_count - count_from_first_tab

add_items_to_cart("https://localhost/3-nowoczesne",count_from_first_tab)
add_items_to_cart("https://localhost/14-lazienkowe",count_from_second_tab)
delete_one_item()
email,password = create_account()
fill_address()
choose_delivery()
choose_payment()
check_status()
