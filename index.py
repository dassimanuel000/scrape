
from cgi import test
import email
from lib2to3.pgen2 import driver
import linecache
import random

from urllib.request import urlopen
from urllib.error import URLError
from urllib.error import HTTPError
from http import HTTPStatus
from urllib.parse import urlparse
from logging import exception
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import Select

################

import sys
from fp.fp import FreeProxy
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time 
from datetime import datetime
from os.path import exists
# pour colorer les prints
from colorama import Fore
from colorama import Style
from urllib.parse import ParseResult, urlparse
from dateutil.relativedelta import relativedelta
import datetime
import requests

# pour colorer les prints
import colorama
import os
import os.path
import re
import time
import json
import pymongo
import json
from pymongo import MongoClient
from pprint import pprint
import urllib.request
from urllib.parse import ParseResult, urlparse
import pandas as pd
import html
import pathlib

import openai
from openai.error import RateLimitError

from ast import literal_eval

import os
sys.setrecursionlimit(10000)


import codecs


def scroll_function(driver, i):
    height = i * 1000
    time.sleep(1.3)
    driver.execute_script("window.scrollTo("+ str(height) +", "+ str(height) +")")
    time.sleep(1.3)
    
# fonction pour donner du délai et cliquer les xpath
def waitBeforeClickOnXpath(driver, xPath):
    time.sleep(1)
    print("clicking on " + xPath + "...")
    button = driver.find_element(By.XPATH, xPath)
    driver.execute_script("arguments[0].click();", button)
    time.sleep(1)
    print("Continue the script")

def waitBeforeClickOnClass(driver, className):
    print("waiting page loading")
    time.sleep(3)
    print("clicking on " + className + "...")
    button = driver.find_element(By.CLASS_NAME, className)
    driver.execute_script("arguments[0].click();", button)
    print("button clicked")
    print("now waiting server response..")
    time.sleep(3)
    print("Continue the script")

def waitBeforeClickOnId(driver, id):
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
def fillById(driver, id, filler):
    print("waiting page loading")
    time.sleep(3)
    driver.find_element(By.ID, id).send_keys(filler)
    print("form filled")
    print("now waiting server response..")
    time.sleep(3)
    print("Continue the script")

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
    print("Complete")
    print("now waiting server response..")
    time.sleep(3)
    print("Continue the script")

def fillByXpath(driver, xpath, filler):
    print("waiting page loading")
    time.sleep(3)
    driver.find_element(By.XPATH, xpath).send_keys(filler)
    time.sleep(3)
    print("Continue the script")

def tryAndRetryClickXpath(driver, xPath):
    try : 
        waitBeforeClickOnXpath(driver, xPath)
    except NoSuchElementException:
        print("the element needs to be charged...")
        time.sleep(10)
        waitBeforeClickOnXpath(driver, xPath)

def tryAndRetryClickClassName(class_name):
    try : 
        waitBeforeClickOnClass(class_name)
    except NoSuchElementException:
        print("the element needs to be charged...")
        time.sleep(10)
        waitBeforeClickOnClass(class_name)

def tryAndRetryClickID(driver, id):
    try : 
        waitBeforeClickOnClass(driver, id)
    except NoSuchElementException:
        print("the element needs to be charged...")
        time.sleep(10)
        waitBeforeClickOnClass(driver, id)


def tryAndRetryFillById(driver, id, value):
    try:
        fillById(driver,id, value)
    except NoSuchElementException:
        print("the element needs to be charged...")
        time.sleep(10)
        fillById(driver,id, value)

def tryAndRetryFillByIdWithSteps(driver, idStep1, id, value):
    try:
        button = driver.find_element(By.ID, idStep1)
        driver.execute_script("arguments[0].click();", button)
        fillById(id, value)
    except NoSuchElementException:
        button = driver.find_element(By.ID, idStep1)
        driver.execute_script("arguments[0].click();", button)
        print("the element needs to be charged...")
        time.sleep(10)
        fillById(id, value)
    except ElementNotInteractableException:
        button = driver.find_element(By.ID, idStep1)
        driver.execute_script("arguments[0].click();", button)
        print("the element needs to be charged...")
        time.sleep(10)
        fillById(id, value)

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
        
def getinnertextXpath(driver, xPath):
    try:
        result = ""
        result = driver.find_element(By.XPATH, xPath)
        result = (result.get_attribute('innerText'))
    except NoSuchElementException:  #spelling error making this code not work as expected
        result = "ZZZZZZZZZZZ"
        pass
    return str(result)


    
def tryAndRetryFillByIdWithExtraSteps(driver, idStep1, id, value):
    try:
        button = driver.find_element(By.ID, idStep1)
        driver.execute_script("arguments[0].click();", button)
        writeLetterByLetterId(id, value)
    except NoSuchElementException:
        button = driver.find_element(By.ID, idStep1)
        driver.execute_script("arguments[0].click();", button)
        print("the element needs to be charged...")
        time.sleep(10)
        writeLetterByLetterId(id, value)
    except ElementNotInteractableException:
        button = driver.find_element(By.ID, idStep1)
        driver.execute_script("arguments[0].click();", button)
        print("the element needs to be charged...")
        time.sleep(10)
        writeLetterByLetterId(id, value)

def tryAndRetryFillByXpath(driver, xpath, value):
    try:
        fillByXpath(driver, xpath, value)
    except NoSuchElementException:
        print("the element needs to be charged...")
        time.sleep(5)
        tryAndRetryFillByXpath(driver, xpath, value)

def if_as_value_FillByXpath(driver, xpath, value):
    if(len(value) > 2):
        try:
            fillByXpath(driver, xpath, value)
        except NoSuchElementException:
            pass
    else:
        pass


def clear_element(driver, xpath):
    elem2 = driver.find_element(By.XPATH, xpath)
    driver.execute_script('arguments[0].value = "";', elem2)

def recaptcha(driver, Xpath):
    try:
        time.sleep(5)
        tryAndRetryClickXpath(driver, Xpath)
        time.sleep(2)
    except NoSuchElementException:
        time.sleep(5)
        
def append_new_line(file_name, text_to_append):
    with open(file_name, "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        file_object.write(text_to_append)

def scroll_function(i, driver):
    height = i * 1000
    time.sleep(1.3)
    driver.execute_script(
        "window.scrollTo(" + str(height) + ", " + str(height) + ")")
    time.sleep(1.3)


TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(description):
    return TAG_RE.sub(' ', description)


def initGoogle(driver):
    cookieGoogle = driver.find_element(By.ID, 'L2AGLb').click()
    try:
        driver.find_element(By.CLASS_NAME, 'h-captcha')
        print(Fore.BLUE + 'Captcha à résoudre veuillez le résoudre et tapez entrez pour continuer...')
        print(Style.RESET_ALL)
    except NoSuchElementException:
        print("No captcha")

    if cookieGoogle:
        print("GOOGLE a changé l'id recupere le nouveau")
    else:
        print("Init Google...")

def findlogo(driver):
    try:
        img_src = driver.find_element(By.XPATH, '(//a[1]//img)')
        img_src = img_src.get_attribute('src')
    except NoSuchElementException:
        img_src = ''
        pass
    return str(img_src)

def findATTR(driver, xpath, attr):
    try:
        value_attr = driver.find_element(By.XPATH, xpath)
        value_attr = value_attr.get_attribute(attr)
    except NoSuchElementException:
        value_attr = ' '
        pass
    return str(value_attr)

def substring_after(s, delim):
    return s.partition(delim)[2]

def count_nombre_de_chiffre(str):
    digit=letter=0
    for ch in str:
        if ch.isdigit():
            digit=digit+1
        elif ch.isalpha():
            letter=letter+1
        else:
            pass
    return digit

def valueifnull(returns, new):
    if returns is None:
        return new
    else:
        returns = str(returns)
        if len(returns.replace(" ", "")) < 4:
            return new
        else:
            return returns


def returnvalueif_delimiter_error(returns, delimiter, new):
    input_string = returns

    slots = input_string.split(delimiter,1)
    if len(slots) > 1:
        return slots[1]
    else:
        return new
    
def solve(x):
    try:
        return literal_eval(x)
    except (ValueError, SyntaxError):
        return x
    
def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
        if True:
            return 0
    except NoSuchElementException:
        return 1



def search_array(list_search, words):
    """if any(words in s for s in list_search):
        print('seeeeeeeeeeeeaaaaaaaaaaarrrrrrrrcccccchhhhhhhhh  ok')
        return 'ok'
    
    else:
        return 'add'"""
    if any(words in word for word in list_search):
        return 11
    else:
        return 22
 
            
        



    
    
def multiselect_set_selections(driver, element_id, labels,tag):
    el = driver.find_element(By.XPATH, element_id)
    for option in el.find_elements(By.TAG_NAME, tag):
        if option.text.strip() in labels.strip():
            option.click()
            
def add_meta(driver, name_input, value):
    multiselect_set_selections(driver, '//select[contains(@id, "metakeyselect")]', name_input, 'option')
    
    tryAndRetryFillByXpath(driver, "//textarea[contains(@id, 'metavalue')]", value)
    tryAndRetryClickXpath(driver, "//input[contains(@id, 'newmeta-submit')]")
    time.sleep(6)



def rediger_article(sujet, ville, number):
    name_e = "E-"+str(number)+".txt"
    
    openai.api_key = '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'  # Remplacez par votre clé API OpenAI

    prompt = f"Bonjour, Peux-tu rédiger un article sur la profession {sujet} en mettant en avant {ville} et expliquer comment elle peut apporter son aide dans ce domaine.\n\n"

    while True:
        try:
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=prompt,
                max_tokens=600,
                n=1,
                stop=None,
                temperature=0.7,
                top_p=0.9,
                frequency_penalty=0.2,
                presence_penalty=0.2
            )

            if 'choices' in response and len(response['choices']) > 0:
                article = response['choices'][0]['text']
                append_new_line(r''+name_e+'', str(article).encode('unicode-escape').decode('utf-8') + "\n \n" + str("Therapeute.net") + "\n")
                return article
            else:
                return None

        except openai.error.RateLimitError as e:
            print(f"Rate limit exceeded. Waiting for {e.retry_after} seconds.")
            time.sleep(360)
            append_new_line(r'ERREUR-IA.txt', str(number)+" "+str(e))
 
    
#browser()
#postbrowser()
def get_website_status(url):
     result = "0"
     # handle connection errors
     try:
          # open a connection to the server with a timeout
          with urlopen(url, timeout=3) as connection:
               # get the response code, e.g. 200
               code = connection.getcode()
               result = (code)
     except HTTPError as e:
          result = "0"
     except URLError as e:
          result = "0"
     except:
          result = "0"
     print(result)
     parsed_uri8888 = urlparse(url)
     result8888 = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri8888)
     hostname8888 = result8888
     list_search.append(hostname8888)
     return str(result)

def finimagerename():
        
    # Chemin vers le dossier contenant les images
    dossier_des_bonnes_images = './I2/'

    # Obtenez la liste des fichiers dans le dossier
    fichiers = os.listdir(dossier_des_bonnes_images)

    # Compteur initial
    compteur = 201
    df = pd.read_excel(r'./data.xlsx')

    # Parcourir chaque fichier dans le dossier
    for fichier in fichiers:
        # Vérifier si le fichier est une image
        if fichier.endswith((".jpg", ".jpeg", ".png", ".gif")):
            # Créer un nouveau nom de fichier avec le compteur
            profession_praticien = str(df.at[compteur, 'profession_praticien'])
            
            ville_praticien = str(df.at[compteur, 'ville_praticien'])
            
            nouveau_nom = f"{profession_praticien}-{ville_praticien}-EE{compteur}.jpg" 
            
            # Chemin complet vers l'ancien et le nouveau fichier
            ancien_chemin = os.path.join(finimagerename, fichier)
            nouveau_chemin = os.path.join(finimagerename, nouveau_nom)
            
            # Renommer le fichier
            os.rename(ancien_chemin, nouveau_chemin)
            
            print(f"{fichier} renommé en {nouveau_nom}")
            
            # Incrémenter le compteur
            compteur += 1
            
                
                
                
                
                
def add_image_listivo(driver, image_link_value, id_post, profession):
    if('data:image' in image_link_value):
        append_new_line(r'all_error.txt', "Image pas mise pour "+id_post)
        pass
    
    else:
        tryAndRetryClickXpath(driver, '//a[contains(@id, "set-post-thumbnail")]')
            
        time.sleep(2)
        try:
            
            tryAndRetryClickXpath(driver, '//button[contains(@id, "menu-item-browse")]')
            tryAndRetryFillByXpath(driver, '//input[contains(@id, "media-search-input")]', str(image_link_value))
            tryAndRetryFillByXpath(driver, '//input[contains(@id, "media-search-input")]', Keys.RETURN)
            
            time.sleep(2)
            if check_exists_by_xpath(driver, '//div[contains(@class, "attachments-wrapper")]//ul//li[1]') == 0:
                time.sleep(3)
            if check_exists_by_xpath(driver, '//div[contains(@class, "attachments-wrapper")]//ul//li[1]') == 0:
                
                if check_exists_by_xpath(driver, '//div[contains(@class, "attachments-wrapper")]//ul//li[contains(@aria-label, "'+str(profession)+'")]') == 0:
                    tryAndRetryClickXpath(driver, '//div[contains(@class, "attachments-wrapper")]//ul//li[contains(@aria-label, "'+str(profession)+'")]')
                else:
                    tryAndRetryClickXpath(driver, '//div[contains(@class, "attachments-wrapper")]//ul//li[1]')
                tryAndRetryClickXpath(driver, '//div[contains(@class, "media-toolbar")]//button[contains(@class, "media-button-select")]')
                tryAndRetryClickXpath(driver, '//div[contains(@id, "wpcontent")]')
            else:
                append_new_line(r'all_error_PRATICIEN.txt', "Image pas mise pour "+id_post)
                
        except NoSuchElementException:
            pass





            
#publish()
def BIG8DONWLOAD():
        
    def download_image(url, file_name):
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                file.write(response.content)
                print(f"{file_name} téléchargé avec succès!")
        else:
            print(f"Échec du téléchargement de {file_name}.")

    # Spécifiez le chemin vers votre fichier texte contenant les liens d'images
    file_path = './liste-img-excel.txt'

    # Vérifier si le fichier existe
    try:
        with open('derniernumer', 'r') as files:
            last_number = int(files.read())
    except FileNotFoundError:
        last_number = 0
    number = last_number + 1
    df = pd.read_excel(r'./data.xlsx')
    
    
def publish():

    input('9999999999999999999999')
    list_search = list()
    my_list = list()
    my_list__ = list()
    final_result = list()
    option = FirefoxOptions()
    option.add_argument('--disable-notifications')
    option.add_argument("--mute-audio")
    #option.add_argument("--headless")
    #option.profile = "C:/Users/admin/AppData/Local/Mozilla/Firefox/Profiles/a2wm8g9y.default"

    option.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")
    
    driverinstance = webdriver.Firefox(options=option)

    
    
while True:
    try:
        publish()
        break
    except Exception as e:
        print("Une erreur s'est produite :", str(e))
        print("Redémarrage du script dans 5 secondes...")
        time.sleep(360)
 