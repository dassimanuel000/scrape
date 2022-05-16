# Python program to explain os.mkdir() method
from itertools import count
from operator import mod
from os import listdir
from os.path import isfile, join
from pprint import pprint
import json
import time
from typing import Any, final
import colorama
from colorama import Fore
from colorama import Style
from pymongo import MongoClient
from selenium.webdriver.common.alert import Alert 
from cgi import test
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import InvalidSelectorException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# importing os module
import os

colorama.init()
# fonction pour donner du délai et cliquer les xpath
def scrollToFindElement(xPathScroll):
    
    element = driver.find_element(By.XPATH, xPathScroll)
    desired_y = (element.size['height'] / 2) + element.location['y']
    current_y = (driver.execute_script('return window.innerHeight') / 2) + driver.execute_script('return window.pageYOffset')
    scroll_y_by = desired_y - current_y
    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)

def waitBeforeClickOnXpath(xPath):
    print("waiting page loading")
    time.sleep(3)
    print("clicking on " + xPath + "...")
    button = driver.find_element(By.XPATH, xPath)
    driver.execute_script("arguments[0].click();", button)
    print("button clicked")
    print("now waiting server response..")
    time.sleep(3)
    print("Continue the script")

def waitBeforeClickOnClass(className):
    print("waiting page loading")
    time.sleep(3)
    print("clicking on " + className + "...")
    button = driver.find_element(By.CLASS_NAME, className)
    driver.execute_script("arguments[0].click();", button)
    print("button clicked")
    print("now waiting server response..")
    time.sleep(3)
    print("Continue the script")

def waitBeforeClickOnId(id):
    print("waiting page loading")
    time.sleep(3)
    print("clicking on " + id + "...")
    button = driver.find_element(By.ID, id)
    driver.execute_script("arguments[0].click();", button)
    print("button clicked")
    print("now waiting server response..")
    time.sleep(3)
    print("Continue the script")

# rempli de texte la case formulaire avec l'id correspondant
def fillById(id, filler):
    print("waiting page loading")
    time.sleep(3)
    driver.find_element(By.ID, id).send_keys(filler)
    print("form filled")
    print("now waiting server response..")
    time.sleep(3)
    print("Continue the script")

def fillByIdWithSteps(id ,filler):
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

def fillByClass(clss ,filler):
    print("waiting page loading")
    time.sleep(3)
    element = driver.find_element_by_class_name(clss).click()
    time.sleep(1)
    element.send_keys(filler)
    print("Fill with our value")
    time.sleep(1)
    print("Complete")
    print("now waiting server response..")
    time.sleep(3)
    print("Continue the script")

def fillByXpath(xpath, filler):
    print("waiting page loading")
    time.sleep(3)
    driver.find_element(By.XPATH, xpath).send_keys(filler)
    print("form filled")
    print("now waiting server response..")
    time.sleep(3)
    print("Continue the script")

def tryAndRetryClickXpath(xPath):
    try : 
        waitBeforeClickOnXpath(xPath)
    except NoSuchElementException:
        print("the element needs to be charged...")
        time.sleep(10)
        waitBeforeClickOnXpath(xPath)

def tryAndRetryClickClassName(class_name):
    try : 
        waitBeforeClickOnClass(class_name)
    except NoSuchElementException:
        print("the element needs to be charged...")
        time.sleep(10)
        waitBeforeClickOnClass(class_name)

def tryAndRetryClickID(id):
    try : 
        waitBeforeClickOnClass(id)
    except NoSuchElementException:
        print("the element needs to be charged...")
        time.sleep(10)
        waitBeforeClickOnClass(id)


def tryAndRetryFillById(id, value):
    try:
        fillById(id, value)
    except NoSuchElementException:
        print("the element needs to be charged...")
        time.sleep(10)
        fillById(id, value)

def writeLetterByLetterId(id, word):
    print("waiting page loading")
    time.sleep(3)
    driver.find_element(By.ID, id).send_keys(Keys.CONTROL + "a")
    print("Taking all that already exist")
    time.sleep(1)
    driver.find_element(By.ID, id).send_keys(Keys.DELETE)
    print("Cleaning")
    for i in word:
        driver.find_element(By.ID, id).send_keys(i)

def tryToFindAndClickCategorie(keyword):
    try:
        testing = driver.find_element(By.XPATH, f"//input[@value='{keyword}']")
        driver.execute_script("arguments[0].click();", testing)
    except NoSuchElementException:
        print("a problem occured...")
        time.sleep(5)
        testing = driver.find_element(By.XPATH, f"//input[@value='{keyword}']")
        driver.execute_script("arguments[0].click();", testing)
    

try:
	client = MongoClient("mongodb://192.168.1.174:27017/")
	print("Connected successfully!!!")
except:
	print("Could not connect to MongoDB")

J = input("Tapez le jour désiré de 01 à 31: \n")
M = input("Tapez le mois désiré de 01 à 12: \n")
date = J+M

pathStockDesJsons = f"C:/Users/admin/Desktop/indeed/stockageOffreIndeed{date}"
os.chdir(pathStockDesJsons)
listeDesJsonStockes = [f for f in listdir(pathStockDesJsons) if isfile(join(pathStockDesJsons, f))]

# print(listeDesJsonStockes[0])
nombreDeBoucles = len(listeDesJsonStockes)
# arrêté à 6 Préparatrice de commande
compteurBoucles = 0
db = client.V2

while compteurBoucles < nombreDeBoucles:
    col = db["regionjob_annonce"]
    col.drop()
    col = db["regionjob_annonce"]
    with open(f"{listeDesJsonStockes[compteurBoucles]}") as file: 
        file_data = json.load(file) 

        try:
            col.insert_many(file_data)
        except:
            try:
                col.insert_one(file_data)
            except TypeError:
                print(Fore.RED + "La stack est vide")
                print(Style.RESET_ALL)
                with open(f'../stackVide/{listeDesJsonStockes[compteurBoucles]}.txt', encoding='utf-8', mode='w') as file:
                    file.write(f"{listeDesJsonStockes[compteurBoucles]}")

    print(Fore.YELLOW + listeDesJsonStockes[compteurBoucles])
    print(Style.RESET_ALL)
    # posteurJsPath = "C:/Users/admin/Desktop/indeed/PosteurJS"
    # os.chdir(posteurJsPath)
    # os.system('start cmd /c "npm start"') 

    launchParamiko = "C:/Users/admin/Desktop/indeed"
    os.chdir(launchParamiko)
    # test 
    os.system('start cmd /k "py .\connectSSH.py"')


    # time.sleep(750)
    print(Fore.RED + "A l'utilisation de mon script soyez extrêmement vigilant à ne pas modifier la commande Taskill...")
    input("Press enter when posting is finished : ...\n")
    print(Style.RESET_ALL)

    # Ne pas toucher
    os.system("taskkill /f /im cmd.exe /t")
    # Ne pas toucher

    os.chdir(pathStockDesJsons)

    input("When you are ready to continue press enter")
    compteurBoucles = compteurBoucles + 1