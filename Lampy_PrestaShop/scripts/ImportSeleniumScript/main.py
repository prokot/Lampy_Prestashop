# coding=utf8
import os
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

driver = webdriver.Chrome(r'/home/lulian/Documents/Lampy_PrestaShop/scripts/ImportSeleniumScript/seleniumdriver/linux/chromedriver')

def importOneFacility(facility,filename):

    time.sleep(1)
    if facility == '0':
        nav = driver.find_element(By.ID,"nav-sidebar")
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", nav)
        
        delay = 100
    
        driver.find_elements(By.CSS_SELECTOR, ".material-icons.mi-settings_applications")[0].click()
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, 'Importuj')))
            print ("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")

        time.sleep(1)

        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", nav)

        driver.find_element(By.LINK_TEXT, 'Importuj').click()

    category = Select(driver.find_element(By.ID, 'entity'))
    category.select_by_value(facility)

    file_upload = driver.find_element(By.ID,"file")

    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", file_upload)
    time.sleep(0.5)
    file_upload.send_keys(os.getcwd()+filename)
    time.sleep(1)

    element = driver.find_element(By.CSS_SELECTOR,"[for='truncate_1']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)
    time.sleep(0.5)

    element.click()

    element2 = driver.find_element(By.CSS_SELECTOR,"[for='forceIDs_1']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element2)
    time.sleep(0.5)

    element2.click()

    submit_button = driver.find_element(By.NAME, "submitImportFile")

    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", submit_button)
    time.sleep(0.5)

    submit_button.click()
    driver.switch_to.alert.accept()

    if facility == '1':
        importConfig = Select(driver.find_element(By.ID,"valueImportMatchs"))
        importConfig.select_by_visible_text("domyslny")

        driver.find_element(By.ID,"loadImportMatchs").click()

    driver.find_element(By.ID,"import").click()

    WebDriverWait(driver, 10000).until(
    EC.element_to_be_clickable((By.ID, "import_close_button")))

    close_button = driver.find_element(By.ID, "import_close_button").click()


driver.maximize_window()
driver.get("http://localhost/admin007k7wti0/")
assert "Imperium Lamp" in driver.title
emailbox = driver.find_element(By.ID,"email")
emailbox.clear()
emailbox.send_keys("julekkrabel@gmail.com")
passwordbox = driver.find_element(By.ID,"passwd")
passwordbox.clear()
passwordbox.send_keys("rootroot")
passwordbox.send_keys(Keys.RETURN)

delay = 6
try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID,"subtab-AdminImport")))
    print ("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

importOneFacility('0',"/categoriesInCSV.csv")
importOneFacility('1',"/productsInCSV.csv")
# import zakonczony
time.sleep(1)

nav = driver.find_element(By.CSS_SELECTOR,".nav-bar-overflow")

driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", nav)

preferences = driver.find_element(By.CSS_SELECTOR,".material-icons.mi-settings")

WebDriverWait(driver, 10).until(
EC.element_to_be_clickable((By.CSS_SELECTOR,".material-icons.mi-settings")))

preferences.click()

driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", nav)


WebDriverWait(driver, 10).until(
EC.element_to_be_clickable((By.LINK_TEXT, 'Szukaj')))
driver.find_element(By.LINK_TEXT, 'Szukaj').click()

indexes = driver.find_element(By.LINK_TEXT,"Przebuduj cały indeks")

driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", indexes)
time.sleep(0.5)

indexes.click()
            
WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.XPATH,"//*[text()='Zaktualizowano pomyślnie.']")))
		
driver.close()
