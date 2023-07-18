import importlib.util
import time

try:
    from headerSelenium import *
except ModuleNotFoundError:
    importlib.util.module_for_loader
    
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import colorama
from colorama import Fore
from colorama import Style

colorama.init()
   
# Fonctions to click elements

# fonction pour donner du délai et cliquer les xpath
def scrollToFindElement(driver, xPathScroll):
    element = driver.find_element(By.XPATH, xPathScroll)
    desired_y = (element.size['height'] / 2) + element.location['y']
    current_y = (driver.execute_script('return window.innerHeight') / 2) + driver.execute_script('return window.pageYOffset')
    scroll_y_by = desired_y - current_y
    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)

def waitBeforeClickOnXpath(driver, xPath):
    print("waiting page loading")
    time.sleep(3)
    print("clicking on " + xPath + "...")
    button = driver.find_element(By.XPATH, xPath)
    driver.execute_script("arguments[0].click();", button)
    print(Fore.RED + "XpathClicked" + Style.RESET_ALL)
    print(Fore.BLUE + "--------------------Phase Completed-------------------\nCharging Next Phase" + Style.RESET_ALL)
    time.sleep(3)

def waitBeforeClickOnClass(driver, className):
    print("waiting page loading")
    time.sleep(3)
    print("clicking on " + className + "...")
    button = driver.find_element(By.CLASS_NAME, className)
    driver.execute_script("arguments[0].click();", button)
    print(Fore.RED + "ClassClicked" + Style.RESET_ALL)
    print(Fore.BLUE + "--------------------Phase Completed-------------------\nCharging Next Phase" + Style.RESET_ALL)
    time.sleep(3)
    

def waitBeforeClickOnId(driver, id):
    print("waiting page loading")
    time.sleep(3)
    print("clicking on " + id + "...")
    button = driver.find_element(By.ID, id)
    driver.execute_script("arguments[0].click();", button)
    print(Fore.RED + "IdClicked" + Style.RESET_ALL)
    print(Fore.BLUE + "--------------------Phase Completed-------------------\nCharging Next Phase" + Style.RESET_ALL)
    time.sleep(3)
    

# rempli de texte la case formulaire avec l'id correspondant
def fillById(driver, id, filler):
    print("waiting page loading")
    time.sleep(3)
    driver.find_element(By.ID, id).send_keys(filler)
    print(Fore.RED + "Form id filled" + Style.RESET_ALL)
    print(Fore.BLUE + "--------------------Phase Completed-------------------\nCharging Next Phase" + Style.RESET_ALL)
    time.sleep(3)

def fillByIdWithSteps(driver, id ,filler):
    print("waiting page loading")
    time.sleep(3)
    driver.find_element(By.ID, id).send_keys(Keys.CONTROL + "a")
    print("Taking all that already exist")
    time.sleep(1)
    driver.find_element(By.ID, id).send_keys(Keys.DELETE)
    print("Cleaning")
    time.sleep(1)
    driver.find_element(By.ID, id).send_keys(filler)
    print("Fill with our value")
    time.sleep(1)
    print("Complete")
    print("now waiting server response..")
    time.sleep(3)
    print("Continue the script")

def fillByClass(driver, clss ,filler):
    print("waiting page loading")
    time.sleep(3)
    element = driver.find_element_by_class_name(clss).click()
    time.sleep(1)
    element.send_keys(filler)
    print("Fill with our value")
    time.sleep(1)
    print(Fore.RED + "Fill by class complete" + Style.RESET_ALL)
    print("now waiting server response..")
    time.sleep(3)
    print("Continue the script")

def fillByXpath(driver, xpath, filler):
    print("waiting page loading")
    time.sleep(3)
    driver.find_element(By.XPATH, xpath).send_keys(filler)
    print(Fore.RED + "Fill by Xpath complete" + Style.RESET_ALL)
    print("now waiting server response..")
    time.sleep(3)
    print("Continue the script")

def tryAndRetryClickXpath(driver, xPath):
    try : 
        waitBeforeClickOnXpath(driver, xPath)
    except NoSuchElementException:
        print("the element needs to be charged...")
        time.sleep(10)
        tryAndRetryClickXpath(driver, xPath)
        
def tryAndRetryClickXpathXTimes(driver, xPath, x):
    i = 0
    while i < x:
        try : 
            waitBeforeClickOnXpath(driver, xPath)
        except NoSuchElementException:
            print("the element needs to be charged...")
            time.sleep(10)
            waitBeforeClickOnXpath(driver, xPath)
        i = i + 1

            
def tryAndRetryClickClassName(driver, class_name):
    try : 
        waitBeforeClickOnClass(driver, class_name)
    except NoSuchElementException:
        print("the element needs to be charged...")
        time.sleep(10)
        tryAndRetryClickClassName(driver, class_name)
        
def tryAndRetryClickClassNameXTimes(driver, class_name, x):
    i = 0
    while i < x:
        try : 
            waitBeforeClickOnClass(driver, class_name)
        except NoSuchElementException:
            print("the element needs to be charged...")
            time.sleep(10)
            waitBeforeClickOnClass(driver, class_name)
        i = i + 1

def tryAndRetryClickID(driver, id):
    try : 
        waitBeforeClickOnId(driver, id)
    except NoSuchElementException:
        print("the element needs to be charged...")
        time.sleep(10)
        try:
            waitBeforeClickOnId(driver, id)
        except NoSuchElementException:
            time.sleep(10)
            tryAndRetryClickID(driver, id)

def tryAndRetryClickIDXTimes(driver, id, x):
    i = 0
    while i < x:
        try : 
            waitBeforeClickOnId(driver, id)
        except NoSuchElementException:
            print("the element needs to be charged...")
            time.sleep(10)
            try:
                waitBeforeClickOnId(driver, id)
            except NoSuchElementException:
                time.sleep(10)
                waitBeforeClickOnId(driver, id)
        i = i + 1


def tryAndRetryFillById(driver, id, value):
    try:
        fillById(driver, id, value)
    except NoSuchElementException:
        print("the element needs to be charged...")
        time.sleep(10)
        tryAndRetryFillById(driver, id, value)
        
def tryAndRetryFillByIdXTimes(driver, id, value, x):
    i = 0
    while i < x:
        try:
            fillById(driver, id, value)
        except NoSuchElementException:
            print("the element needs to be charged...")
            time.sleep(10)
            fillById(driver, id, value)
        i = i + 1
        
def tryAndRetryFillByXpath(driver, xpath, value):
    try:
        fillByXpath(driver, xpath, value)
    except NoSuchElementException:
        print("the element needs to be charged...")
        time.sleep(10)
        tryAndRetryFillByXpath(driver, xpath, value)
        
def tryAndRetryFillByXpathXtimes(driver, xpath, value, x):
    i = 0
    while i < x:
        try:
            fillByXpath(driver, xpath, value)
        except NoSuchElementException:
            print("the element needs to be charged...")
            time.sleep(10)
            fillByXpath(driver, xpath, value)
        i = i + 1


def writeLetterByLetterId(driver, id, word):
    print("waiting page loading")
    time.sleep(3)
    driver.find_element(By.ID, id).send_keys(Keys.CONTROL + "a")
    print("Taking all that already exist")
    time.sleep(1)
    driver.find_element(By.ID, id).send_keys(Keys.DELETE)
    print("Cleaning")
    for i in word:
        driver.find_element(By.ID, id).send_keys(i)

def tryToFindAndClickCategorie(driver, keyword):
    try:
        testing = driver.find_element(By.XPATH, f"//input[@value='{keyword}']")
        driver.execute_script("arguments[0].click();", testing)
    except NoSuchElementException:
        print("a problem occured...")
        time.sleep(5)
        testing = driver.find_element(By.XPATH, f"//input[@value='{keyword}']")
        driver.execute_script("arguments[0].click();", testing)