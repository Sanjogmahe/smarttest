# from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.alert import Alert
from datetime import date
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

today = date.today()

# dd/mm/YY
d1 = today.strftime("%m/%d/%Y")


options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors')
#options.add_argument('--headless')
#options.add_argument("--lang=en")
options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
options.add_argument('--disable-dev-shm-usage')
# options.binary_location = "M:/Application/chrome.exe"
driver = webdriver.Chrome(options=options, executable_path="C:/Users/azure/PycharmProjects/SmartTest/chromedriver.exe")
driver.maximize_window()


def CancelAlert():
    click_alert = driver.switch_to.alert
    click_alert.accept()

def key():
    driver.send_Keys(Keys.chord(Keys.CONTROL, "a"), "2020-11-02 17:00 to 2020-11-02 20:10");

def xp():
    button = driver.find_element_by_xpath("//span[text()='sla28565.srv.allianz']")
    driver.execute_script("arguments[0].click();", button)

def xp1():
    button = driver.find_element_by_xpath("//div[@class='gwt-Label dht-db']")
    driver.execute_script("arguments[0].click();", button)

def arg(xpath):
    button = driver.find_element_by_xpath(xpath)
    driver.execute_script("arguments[0].click();", button)

def el_id(x):
    driver.find_element(By.XPATH, x)

def triel(y):
    clean=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, y)))
    clean.click()
    clean.clear()

def waituntil(y):
    clean = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, y)))
    clean.click()
    # Next = driver.find_element_by_xpath("//div[@class='gwt-Label dIb-a'][contains(text(),'Custom')]")
    # driver.execute_script("arguments[0].clear();", Next)

def capa():
    capabilities = webdriver.DesiredCapabilities().CHROME
    capabilities['acceptSslCerts'] = True

    driver = webdriver.chrome(capabilities=capabilities)
    driver.get('https://cacert.org/')



def url(link):
    driver.get(
        link)

testStep=[]
transactionName=[]
testData=[]

def justCli(Xpath):
    driver.find_element(By.XPATH, Xpath).click()
    driver.implicitly_wait(50)

def cli(Xpath):
    text = driver.find_element(By.XPATH, Xpath).get_attribute('innerHTML')
    driver.find_element(By.XPATH, Xpath).click()
    testStep.append("Click on " + text + ' button')
    transactionName.append("_Claws_CloseSuffix_" + "Click on " + text)
    testData.append("")
    driver.implicitly_wait(50)

def justEnt(Xpath ,details):
    driver.find_element(By.XPATH, Xpath).send_keys(details)
    time.sleep(1)
    #driver.implicitly_wait(70)

def sendkey(Xpath):
    driver.find_element(By.XPATH, Xpath).send_keys(u'\ue007')
    time.sleep(1)

def ent(Xpath ,details):
    text = driver.find_element(By.XPATH, Xpath).get_attribute('id')
    driver.find_element(By.XPATH, Xpath).send_keys(details)
    testStep.append("Enter " + details + " in " + text)
    transactionName.append("_Claws_CloseSuffix_" + "enter_" + details)
    testData.append(text+" : "+details)
    time.sleep(1)
    #driver.implicitly_wait(70)

def hover(xpath):
    check = driver.find_element(By.XPATH, xpath)
    hover = ActionChains(driver).move_to_element(check)
    hover.perform()

def clear(xpath):
    driver.find_element(By.XPATH, xpath).clear()
    time.sleep(1)

def wait(x):
    driver.implicitly_wait(x)

def ewait(x):
    import time
    time.sleep(x)

def iframe(frame):
    ifram = driver.find_element(By.XPATH, frame)
    driver.switch_to.frame(ifram)

def default_iframe():
    driver.switch_to.default_content()

# def soupContent():
#     content = driver.page_source
#     soup = BeautifulSoup(content, features="html5lib")
#     return soup


def alertHandle():
    alert = Alert(driver)
    alert.accept()
def quit():
    driver.quit()