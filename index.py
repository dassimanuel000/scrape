
from cgi import test
import email
from lib2to3.pgen2 import driver
import linecache
import random
import subprocess

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
from datetime import datetime

sys.setrecursionlimit(10000)
nows = datetime.utcnow()


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
    time.sleep(3)
    el = driver.find_element(By.XPATH, xpath)
    for character in filler:
        el.send_keys(character)
        time.sleep(0.3) # pause for 0.3 seconds
    time.sleep(3)

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
        result = " "
        pass
    if result == " ":
        time.sleep(2)
        try:
            result = ""
            result = driver.find_element(By.XPATH, xPath)
            result = (result.get_attribute('innerText'))
        except NoSuchElementException:  #spelling error making this code not work as expected
            result = " "
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
        time.sleep(3)
        waitBeforeClickOnXpath(driver, Xpath)
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
    driver.get("https://www.google.com/")
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

def valueifnull(returns, new): #valueifnull(line_value.get("FACEBOOK"), ' ')
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




def waitloading(times, driverinstance):
    times = int(times)
    time.sleep(times)
    wait = WebDriverWait(driverinstance, times)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
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




def scrap_site_saveAnnonceIndeed(profession, ville,categories_path, lieu_tres_precis_path, date, etape_processus ):

    if len(profession) > 2 and etape_processus <= 1:
        
        option = FirefoxOptions()
        option.add_argument('--disable-notifications')
        option.add_argument("--mute-audio")
        option.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")
        driverinstance = webdriver.Firefox(options=option)

        initGoogle(driverinstance)
        
        try:
            urlParent = 'https://fr.indeed.com/jobs?q='+profession+'&l='+ville
            urlParent = urlParent + "&fromage=3&limit=25&sort=date&filter=0"
            
            driverinstance.get(urlParent)
            waitloading(2, driverinstance)
            tryAndRetryClickXpath(driverinstance, '//button[contains(@id, "onetrust-reject-all-handler")]')
            
            waitloading(2, driverinstance)
            
            my_list = list()
            final_result = list()

            links = driverinstance.find_elements(By.XPATH,"//body//a[contains(@class, 'jcs-JobTitle')]")
                
            if len(links) == 0:
                print("Aucun lien trouvé.")
            else:
                for i in links:
                    step1 = (i.get_attribute('href'))
                    my_list.append(step1)
                    
                if len(my_list) > 10:
                    my_list = my_list[:10]
                print("----------------------------------"+str(len(my_list))+"-----------------------------------------")
                for j in my_list:
                    driverinstance.get(j)
                    waitloading(2, driverinstance)
                    date_offre = nows.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

                    myDict = {}
                    myDict["date"] = date_offre
                    myDict["url"] = str(j)
                    myDict["titre"]  = remove_tags(getinnertextXpath(driverinstance, "//h1[contains(@class, 'jobsearch-JobInfoHeader-title')]"))


                    myDict["contrat"] = remove_tags(getinnertextXpath(driverinstance, "//div[contains(text(), 'Type de poste')]/following-sibling::div"))



                    myDict["ville"] =  remove_tags(getinnertextXpath(driverinstance, "//div[contains(@data-testid, 'jobsearch-CompanyInfoContainer')]//div[contains(@data-testid, 'inlineHeader-companyLocation')]"))
                    myDict["description"] = remove_tags(getinnertextXpath(driverinstance, "//div[contains(@id, 'jobDescriptionText')]")).encode('unicode-escape').decode('utf-8')
                    myDict["salary"] = remove_tags(getinnertextXpath(driverinstance, "//div[contains(text(), 'Salaire')]/following-sibling::div"))
                    myDict["experience"] = ""
                    myDict["metier"] = ""
                    myDict["statut"] = ""
                    myDict["secteur"] = ""
                    myDict["cats"] = lieu_tres_precis_path
                    myDict["places"] = categories_path
                    myDict["compagny"] = remove_tags(getinnertextXpath(driverinstance, "//div[contains(@data-testid, 'inlineHeader-companyName')]"))
                    myDict["postTime"] = ""


                    
                    name_e = str(date)+"-data.txt"
                    append_new_line(r''+name_e+'', str(myDict).encode('unicode-escape').decode('utf-8'))
                    final_result.append(myDict)
                                
                if len(final_result) > 0:
                    final_result = json.dumps(final_result)
                    final_result = (json.loads(final_result))


                    # Connexion au serveur MongoDB
                    client = pymongo.MongoClient("mongodb://192.168.1.174:27017")

                    # Vérification de l'existence de la base de données "TOUTE_OFFRE"
                    if "TOUTE_OFFRE" in client.list_database_names():
                        # Connexion à la base de données "TOUTE_OFFRE"
                        db = client["TOUTE_OFFRE"]
                    else:
                        # Création de la base de données "TOUTE_OFFRE"
                        db = client["TOUTE_OFFRE"]
                        print("La base de données 'TOUTE_OFFRE' a été créée")

                    # Connexion à la collection "2022-05-15" dans la base de données
                    collection = db[date]
                    collection.insert_many(final_result)
                else:
                    pass
            driverinstance.quit()

        except NoSuchElementException:
            pass



        dernier_etape_processus = date+".txt"
        with open(dernier_etape_processus, 'w') as file:
            file.write(str("2"))

    



def scrap_site_saveAnnoncePE(profession, ville,categories_path, lieu_tres_precis_path, date, etape_processus ):


    if len(profession) > 2 and etape_processus <= 2:
        
        option = FirefoxOptions()
        option.add_argument('--disable-notifications')
        option.add_argument("--mute-audio")
        option.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")
        driverinstance = webdriver.Firefox(options=option)

        initGoogle(driverinstance)
        
        try:
            driverinstance.get("https://candidat.pole-emploi.fr/offres/emploi")
            waitloading(2, driverinstance)
            tryAndRetryClickXpath(driverinstance, '//button[contains(@id, "footer_tc_privacy_button_2")]')
            
            waitloading(2, driverinstance)
            if ville == 'Télétravail':
                tryAndRetryFillByXpath(driverinstance, '//input[contains(@id, "idmotsCles-selectized")]', str(profession))
                tryAndRetryFillByXpath(driverinstance, '//input[contains(@id, "idmotsCles-selectized")]', Keys.RETURN)
                tryAndRetryFillByXpath(driverinstance, '//input[contains(@id, "idmotsCles-selectized")]', str(ville))
                tryAndRetryFillByXpath(driverinstance, '//input[contains(@id, "idmotsCles-selectized")]', Keys.RETURN)
            else:
                tryAndRetryFillByXpath(driverinstance, '//input[contains(@id, "idmotsCles-selectized")]', str(profession))
                tryAndRetryFillByXpath(driverinstance, '//input[contains(@id, "idmotsCles-selectized")]', Keys.RETURN)
                tryAndRetryFillByXpath(driverinstance, '//input[contains(@id, "idlieux-selectized")]', str(ville.split(' - ')[0]))
                tryAndRetryFillByXpath(driverinstance, '//input[contains(@id, "idlieux-selectized")]', Keys.RETURN)

            tryAndRetryClickXpath(driverinstance, '//a[contains(@id, "btnSubmitRechercheForm")]')
            waitloading(2, driverinstance)
            
            
            my_list = list()
            final_result = list()
            for i in range(2):
                recaptcha(driverinstance, '//*[contains(@class, "results-more")]//a')
                waitloading(1, driverinstance)

            links = driverinstance.find_elements(By.XPATH,"//ul[contains(@class, 'result-list')]//a[contains(@class, 'media with-fav')]")
                
            if len(links) == 0:
                print("Aucun lien trouvé.")
            else:
                for i in links:
                    step1 = (i.get_attribute('href'))
                    my_list.append(step1)
                    
                if len(my_list) > 7:
                    my_list = my_list[:7]
                print("----------------------------------"+str(len(my_list))+"-----------------------------------------")
                for j in my_list:
                    driverinstance.get(j)
                    waitloading(2, driverinstance)
                    date_offre = nows.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

                    myDict = {}
                    myDict["date"] = date_offre
                    myDict["url"] = str(j)
                    myDict["titre"]  = remove_tags(getinnertextXpath(driverinstance, "//h1"))
                    myDict["titre"]  = re.sub(r"^Offre n° \d+\n", "", myDict["titre"])

                    myDict["contrat"] = remove_tags(getinnertextXpath(driverinstance, "//div[contains(@class, 'description-aside') and contains(@class, 'col-sm-4') and contains(@class, 'col-md-5')]/dl/dd[5]"))
                    myDict["ville"] =  remove_tags(getinnertextXpath(driverinstance, "//p[contains(@class, 't4') and contains(@class, 'title-complementary')]/span[1]"))
                    myDict["description"] = remove_tags(getinnertextXpath(driverinstance, "//div/div/div/div/div/div/div/div/div/div/div[contains(@class, 'description')]/p")).encode('unicode-escape').decode('utf-8')
                    myDict["salary"] = remove_tags(getinnertextXpath(driverinstance, "//div[contains(@class, 'description-aside') and contains(@class, 'col-sm-4') and contains(@class, 'col-md-5')]/dl/dd[7]/ul/li"))
                    myDict["experience"] = remove_tags(getinnertextXpath(driverinstance, "//li/span/span[contains(@class, 'skill-name')]"))
                    myDict["metier"] = ""
                    myDict["statut"] = ""
                    myDict["secteur"] = ""
                    myDict["cats"] = lieu_tres_precis_path
                    myDict["places"] = categories_path
                    myDict["compagny"] = ""
                    myDict["postTime"] = remove_tags(getinnertextXpath(driverinstance, "//p[contains(@class, 't5') and contains(@class, 'title-complementary')]/span[1]"))
                    myDict["postTime"] = ''.join(c for c in myDict["postTime"] if not c.isalpha())


                    
                    name_e = str(date)+"-data.txt"
                    append_new_line(r''+name_e+'', str(myDict).encode('unicode-escape').decode('utf-8'))
                    final_result.append(myDict)
                                
                if len(final_result) > 0:
                    final_result = json.dumps(final_result)
                    final_result = (json.loads(final_result))


                    # Connexion au serveur MongoDB
                    client = pymongo.MongoClient("mongodb://192.168.1.174:27017")

                    # Vérification de l'existence de la base de données "TOUTE_OFFRE"
                    if "TOUTE_OFFRE" in client.list_database_names():
                        # Connexion à la base de données "TOUTE_OFFRE"
                        db = client["TOUTE_OFFRE"]
                    else:
                        # Création de la base de données "TOUTE_OFFRE"
                        db = client["TOUTE_OFFRE"]
                        print("La base de données 'TOUTE_OFFRE' a été créée")

                    # Connexion à la collection "2022-05-15" dans la base de données
                    collection = db[date]
                    collection.insert_many(final_result)
                else:
                    pass
            driverinstance.quit()

        except NoSuchElementException:
            pass



        dernier_etape_processus = date+".txt"
        with open(dernier_etape_processus, 'w') as file:
            file.write(str("3"))

    
    
def scrap_site_saveAnnonceAPEC(profession, ville,categories_path, lieu_tres_precis_path, date, etape_processus ):

    if len(profession) > 2 and etape_processus <= 3:
        
        option = FirefoxOptions()
        option.add_argument('--disable-notifications')
        option.add_argument("--mute-audio")
        option.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")
        driverinstance = webdriver.Firefox(options=option)

        initGoogle(driverinstance)
        
        try:
            driverinstance.get("https://www.apec.fr/candidat.html")
            waitloading(2, driverinstance)
            tryAndRetryClickXpath(driverinstance, '//div[contains(@id, "onetrust-button-group")]//button[contains(@id, "onetrust-accept-btn-handler")]')
            tryAndRetryFillByXpath(driverinstance, '//div[contains(@class, "offer-search")]//input[contains(@id, "keywords")]', str(profession))
            tryAndRetryFillByXpath(driverinstance, '//div[contains(@class, "offer-search")]//input[contains(@id, "keywords")]', Keys.TAB)
            tryAndRetryFillByXpath(driverinstance, '//div[contains(@class, "offer-search")]//input[contains(@id, "locationOffres")]', str(ville))
            tryAndRetryFillByXpath(driverinstance, '//div[contains(@class, "offer-search")]//input[contains(@id, "locationOffres")]', Keys.RETURN)
            tryAndRetryFillByXpath(driverinstance, '//div[contains(@class, "offer-search")]//input[contains(@id, "locationOffres")]', Keys.RETURN)
            waitloading(2, driverinstance)
            if ville == 'Télétravail':
                teleUrl = driverinstance.current_url
                teleUrl = teleUrl + "&typesTeletravail=20766&typesTeletravail=20765&typesTeletravail=20767"
                driverinstance.get(teleUrl)
                waitloading(3, driverinstance)
            
            
            my_list = list()
            final_result = list()

            links = driverinstance.find_elements(By.XPATH,"//*[contains(@class, 'container-result')]//div//a")
                
            if len(links) == 0:
                print("Aucun lien trouvé.")
            else:
                for i in links:
                    step1 = (i.get_attribute('href'))
                    my_list.append(step1)
                    
                if len(my_list) > 7:
                    my_list = my_list[:7]
                print("----------------------------------"+str(len(my_list))+"-----------------------------------------")
                for j in my_list:
                    driverinstance.get(j)
                    waitloading(2, driverinstance)
                    date_offre = nows.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

                    myDict = {}
                    myDict["date"] = date_offre
                    myDict["url"] = str(j)
                    myDict["titre"]  = remove_tags(getinnertextXpath(driverinstance, "//nav//div//h1"))


                    myDict["contrat"] = remove_tags(getinnertextXpath(driverinstance, "//div[contains(@class, 'card-offer__text')]//ul[contains(@class, 'details-offer-list')]//li[2]"))
                    myDict["ville"] =  remove_tags(getinnertextXpath(driverinstance, "//div[contains(@class, 'card-offer__text')]//ul[contains(@class, 'details-offer-list')]//li[3]"))
                    myDict["description"] = remove_tags(getinnertextXpath(driverinstance, "//apec-poste-informations//div[contains(@class, 'col-lg-8')]//div[contains(@class, 'details-post')]")).encode('unicode-escape').decode('utf-8')
                    myDict["salary"] = remove_tags(getinnertextXpath(driverinstance, "//div[contains(@class, 'col-lg-4')]//div[contains(@class, 'details-post')][1]//span"))
                    myDict["experience"] = remove_tags(getinnertextXpath(driverinstance, "//div[contains(@class, 'col-lg-4')]//div[contains(@class, 'details-post')][3]//span"))
                    myDict["metier"] = remove_tags(getinnertextXpath(driverinstance, "//div[contains(@class, 'col-lg-4')]//div[contains(@class, 'details-post')][4]//span"))
                    myDict["statut"] = remove_tags(getinnertextXpath(driverinstance, "//div[contains(@class, 'col-lg-4')]//div[contains(@class, 'details-post')][6]//span"))
                    myDict["secteur"] = remove_tags(getinnertextXpath(driverinstance, "//div[contains(@class, 'col-lg-4')]//div[contains(@class, 'details-post')][5]//span"))
                    myDict["cats"] = lieu_tres_precis_path
                    myDict["places"] = categories_path
                    myDict["compagny"] = remove_tags(getinnertextXpath(driverinstance, "//div[contains(@class, 'card-offer__text')]//ul[contains(@class, 'details-offer-list')]//li[1]"))
                    myDict["postTime"] = remove_tags(getinnertextXpath(driverinstance, "//div[contains(@class, 'mb-10')]//div//div[contains(@class, 'date-offre')][2]"))
                    myDict["postTime"] = ''.join(c for c in myDict["postTime"] if not c.isalpha())


                    
                    name_e = str(date)+"-data.txt"
                    append_new_line(r''+name_e+'', str(myDict).encode('unicode-escape').decode('utf-8'))
                    final_result.append(myDict)
                                
                if len(final_result) > 0:
                    final_result = json.dumps(final_result)
                    final_result = (json.loads(final_result))


                    # Connexion au serveur MongoDB
                    client = pymongo.MongoClient("mongodb://192.168.1.174:27017")

                    # Vérification de l'existence de la base de données "TOUTE_OFFRE"
                    if "TOUTE_OFFRE" in client.list_database_names():
                        # Connexion à la base de données "TOUTE_OFFRE"
                        db = client["TOUTE_OFFRE"]
                    else:
                        # Création de la base de données "TOUTE_OFFRE"
                        db = client["TOUTE_OFFRE"]
                        print("La base de données 'TOUTE_OFFRE' a été créée")

                    # Connexion à la collection "2022-05-15" dans la base de données
                    collection = db[date]
                    collection.insert_many(final_result)
                else:
                    pass
            driverinstance.quit()

        except NoSuchElementException:
            pass



        dernier_etape_processus = date+".txt"
        with open(dernier_etape_processus, 'w') as file:
            file.write(str("4"))




def scrap_site_saveAnnonceHelloWork(profession, ville,categories_path, lieu_tres_precis_path, date, etape_processus ):

    if len(profession) > 2 and etape_processus <= 4:
        
        option = FirefoxOptions()
        option.add_argument('--disable-notifications')
        option.add_argument("--mute-audio")
        option.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")
        driverinstance = webdriver.Firefox(options=option)

        initGoogle(driverinstance)
        
        try:
            driverinstance.get("https://www.hellowork.com/fr-fr")
            waitloading(2, driverinstance)
            tryAndRetryClickXpath(driverinstance, '//div[contains(@class, "hw-cc-btn-group")]//button[contains(@id, "hw-cc-notice-accept-btn")]')
            waitloading(1, driverinstance)
            tryAndRetryFillByXpath(driverinstance, '//div[contains(@class, "")]//input[contains(@name, "k")]', str(profession))
            tryAndRetryFillByXpath(driverinstance, '//div[contains(@class, "")]//input[contains(@name, "k")]', Keys.TAB)
            tryAndRetryFillByXpath(driverinstance, '//div[contains(@class, "")]//input[contains(@name, "k")]', Keys.TAB)
            if ville == 'Télétravail':
                tryAndRetryFillByXpath(driverinstance, '//div[contains(@class, "")]//input[@name="k"]', Keys.ENTER)
                waitloading(2, driverinstance)
                teleUrl = driverinstance.current_url
                teleUrl = teleUrl + "&t=Complet&t=Partiel&t=Occasionnel&c=CDI&c=CDD"
                driverinstance.get(teleUrl)
                waitloading(3, driverinstance)
            else:
                tryAndRetryFillByXpath(driverinstance, '//div[contains(@class, "")]//input[@name="l"]', str(ville))
                tryAndRetryFillByXpath(driverinstance, '//div[contains(@class, "")]//input[@name="l"]', Keys.ARROW_DOWN)
                tryAndRetryFillByXpath(driverinstance, '//div[contains(@class, "")]//input[@name="l"]', Keys.RETURN)
                waitloading(2, driverinstance)
            
            
            my_list = list()
            final_result = list()

            links = driverinstance.find_elements(By.XPATH,"//section//ul[contains(@data-teleport-target, 'destination')]//li//span//h3//a")
                
            if len(links) == 0:
                print("Aucun lien trouvé.")
            else:
                for i in links:
                    step1 = (i.get_attribute('href'))
                    my_list.append(step1)
                    
                if len(my_list) > 7:
                    my_list = my_list[:7]
                print("----------------------------------"+str(len(my_list))+"-----------------------------------------")
                for j in my_list:
                    driverinstance.get(j)
                    waitloading(2, driverinstance)
                    date_offre = nows.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

                    myDict = {}
                    myDict["date"] = date_offre
                    myDict["url"] = str(j)
                    myDict["titre"]  = remove_tags(getinnertextXpath(driverinstance, "//h1//span"))


                    myDict["contrat"] = remove_tags(getinnertextXpath(driverinstance, "//h1/following-sibling::ul//li[2]//span"))
                    myDict["ville"] =  remove_tags(getinnertextXpath(driverinstance, "//h1/following-sibling::ul//li[1]//span"))
                    myDict["description"] = remove_tags(getinnertextXpath(driverinstance,"//section[contains(@class, 'content modal')]")).encode('unicode-escape').decode('utf-8')
                    myDict["salary"] = remove_tags(getinnertextXpath(driverinstance, "//h1/following-sibling::ul//li[3]//span"))
                    myDict["experience"] = remove_tags(getinnertextXpath(driverinstance, "//section[contains(@class, 'shrink retrait modal')]//ul[2]//li[3]"))
                    myDict["metier"] = remove_tags(getinnertextXpath(driverinstance, "//section[contains(@class, 'shrink retrait modal')]//ul[2]//li[1]"))
                    myDict["statut"] = ""
                    myDict["secteur"] = remove_tags(getinnertextXpath(driverinstance, "//section[contains(@data-company-badge, '')]//ul//li[2]"))
                    myDict["cats"] = lieu_tres_precis_path
                    myDict["places"] = categories_path
                    myDict["compagny"] = remove_tags(getinnertextXpath(driverinstance, "//section[contains(@class, 'content modal')]//h2[1]")).replace("recherche", "").replace("...", "")
                    myDict["postTime"] = remove_tags(getinnertextXpath(driverinstance, "//section[contains(@class, 'shrink retrait modal')]//span[contains(@class, 'retrait')]//span"))
                    myDict["postTime"] = ''.join(c for c in myDict["postTime"] if not c.isalpha())


                    
                    name_e = str(date)+"-data.txt"
                    append_new_line(r''+name_e+'', str(myDict).encode('unicode-escape').decode('utf-8'))
                    final_result.append(myDict)
                                
                if len(final_result) > 0:
                    final_result = json.dumps(final_result)
                    final_result = (json.loads(final_result))


                    # Connexion au serveur MongoDB
                    client = pymongo.MongoClient("mongodb://192.168.1.174:27017")

                    # Vérification de l'existence de la base de données "TOUTE_OFFRE"
                    if "TOUTE_OFFRE" in client.list_database_names():
                        # Connexion à la base de données "TOUTE_OFFRE"
                        db = client["TOUTE_OFFRE"]
                    else:
                        # Création de la base de données "TOUTE_OFFRE"
                        db = client["TOUTE_OFFRE"]
                        print("La base de données 'TOUTE_OFFRE' a été créée")

                    # Connexion à la collection "2022-05-15" dans la base de données
                    collection = db[date]
                    collection.insert_many(final_result)
                else:
                    pass
            driverinstance.quit()

        except NoSuchElementException:
            pass



        dernier_etape_processus = date+".txt"
        with open(dernier_etape_processus, 'w') as file:
            file.write(str("5"))



    
    



def scrap_site_FranceEmploi(profession, ville,categories_path, lieu_tres_precis_path, date, etape_processus ):

    if len(profession) > 2:
        
        option = FirefoxOptions()
        option.add_argument('--disable-notifications')
        option.add_argument("--mute-audio")
        option.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")
        driverinstance = webdriver.Firefox(options=option)
        initGoogle(driverinstance)
    
    




def scrap_site_LINKEDIN(profession, ville,categories_path, lieu_tres_precis_path, date, etape_processus ):

    if len(profession) > 2 and etape_processus <= 6:
        
        option = FirefoxOptions()
        option.add_argument('--disable-notifications')
        option.add_argument("--mute-audio")
        option.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")
        driverinstance = webdriver.Firefox(options=option)

        initGoogle(driverinstance)
        
        try:
            driverinstance.get("https://fr.linkedin.com/jobs/search")
            waitloading(2, driverinstance)
            tryAndRetryClickXpath(driverinstance, "//button[contains(@data-control-name,'ga-cookie.consent.accept.v4')]")
            waitloading(1, driverinstance)
            
            tryAndRetryFillByXpath(driverinstance, '//input[contains(@aria-controls, "job-search-bar-keywords-typeahead-list")]', str(profession)+ " ")
            tryAndRetryFillByXpath(driverinstance, '//input[contains(@aria-controls, "job-search-bar-location-typeahead-list")]', str(ville) + " ")
            
            tryAndRetryFillByXpath(driverinstance, '//input[contains(@aria-controls, "job-search-bar-location-typeahead-list")]', Keys.ENTER)
            time.sleep(3)
            waitloading(3, driverinstance)
            
            my_list = list()
            final_result = list()
     
            links = driverinstance.find_elements(By.XPATH, '//a[contains(@data-tracking-control-name, "public_jobs_jserp-result_search-card")]')
            count = (len(links))
            if count < 4:
                time.sleep(2)
                links = driverinstance.find_elements(By.XPATH,'//a[contains(@data-tracking-control-name, "public_jobs_jserp-result_search-card")]')
                count = (len(links))
                print(count)
            else:
                print(count)


            if len(links) == 0:
                print("Aucun lien trouvé.")
            else:
                for i in links:
                    step1 = (i.get_attribute('href'))
                    my_list.append(step1)
                    
                if len(my_list) > 5:
                    my_list = my_list[:5]
                print("----------------------------------"+str(len(my_list))+"-----------------------------------------")
                for j in my_list:
                    driverinstance.get(j)
                    waitloading(1, driverinstance)
                    date_offre = nows.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

                    myDict = {}
                    myDict["date"] = date_offre
                    myDict["url"] = str(j)
                    myDict["titre"]  = remove_tags(getinnertextXpath(driverinstance, '//div[contains(@class, "top-card-layout__entity-info")]//h1'))


                    myDict["contrat"] = remove_tags(getinnertextXpath(driverinstance, '//span[contains(@class, "description__job-criteria-text--criteria")][2]'))
                    myDict["ville"] =  remove_tags(getinnertextXpath(driverinstance, '//div[contains(@class, "topcard__flavor-row")][1]//span[contains(@class, "topcard__flavor--bullet")]'))
                    myDict["salary"] = ""
                    myDict["experience"] = remove_tags(getinnertextXpath(driverinstance, '//span[contains(@class, "description__job-criteria-text--criteria")][1]'))
                    myDict["metier"] = remove_tags(getinnertextXpath(driverinstance, '//span[contains(@class, "description__job-criteria-text--criteria")][3]'))
                    myDict["statut"] = ""
                    myDict["secteur"] = remove_tags(getinnertextXpath(driverinstance, '//span[contains(@class, "description__job-criteria-text--criteria")][4]'))
                    myDict["cats"] = lieu_tres_precis_path
                    myDict["places"] = categories_path
                    myDict["compagny"] = ""
                    myDict["postTime"] = ""
 
                    myDict["description"] = remove_tags(getinnertextXpath(driverinstance, '//section[contains(@class, "show-more-less-html")]//div[contains(@class, "show-more-less-html__markup")]')).encode('unicode-escape').decode('utf-8')
                    

                    
                    name_e = str(date)+"-data.txt"
                    append_new_line(r''+name_e+'', str(myDict).encode('unicode-escape').decode('utf-8'))
                    final_result.append(myDict)
                                
                if len(final_result) > 0:
                    final_result = json.dumps(final_result)
                    final_result = (json.loads(final_result))


                    # Connexion au serveur MongoDB
                    client = pymongo.MongoClient("mongodb://192.168.1.174:27017")

                    # Vérification de l'existence de la base de données "TOUTE_OFFRE"
                    if "TOUTE_OFFRE" in client.list_database_names():
                        # Connexion à la base de données "TOUTE_OFFRE"
                        db = client["TOUTE_OFFRE"]
                    else:
                        # Création de la base de données "TOUTE_OFFRE"
                        db = client["TOUTE_OFFRE"]
                        print("La base de données 'TOUTE_OFFRE' a été créée")

                    # Connexion à la collection "2022-05-15" dans la base de données
                    collection = db[date]
                    collection.insert_many(final_result)
                else:
                    pass

        except NoSuchElementException:
            pass
        
        driverinstance.quit()



        dernier_etape_processus = date+".txt"
        with open(dernier_etape_processus, 'w') as file:
            file.write(str("7"))
    

def scrap_site_JobUp(profession, ville,categories_path, lieu_tres_precis_path, date, etape_processus ):

    
    if len(profession) > 2 and etape_processus <= 7:
        
        option = FirefoxOptions()
        option.add_argument('--disable-notifications')
        option.add_argument("--mute-audio")
        option.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")
        driverinstance = webdriver.Firefox(options=option)

        initGoogle(driverinstance)
        
        try:
            driverinstance.get("https://www.jobup.ch/")
            waitloading(1, driverinstance)
            driverinstance.get("https://www.jobup.ch/fr/emplois/")
            waitloading(2, driverinstance)
            tryAndRetryClickXpath(driverinstance, '//div[contains(@id, "modal")]//div//div//div//div//button[contains(@type, "button")]//span')
            waitloading(1, driverinstance)
            if ville == 'Télétravail':
                teleUrl = driverinstance.current_url
                teleUrl = teleUrl + "?benefit=1&term="
                driverinstance.get(teleUrl)
                waitloading(3, driverinstance)
            elif ville == 'Genève' and profession == 'Assistant administratif':
                teleUrl = driverinstance.current_url
                teleUrl = teleUrl + "?employment-type=5&employment-type=1&location=Genève&publication-date=1"
                driverinstance.get(teleUrl)
                waitloading(3, driverinstance)
            else:
                tryAndRetryFillByXpath(driverinstance, '//input[contains(@id, "synonym-typeahead-text-field")]', str(profession))
                tryAndRetryFillByXpath(driverinstance, '//input[contains(@id, "synonym-typeahead-text-field")]', Keys.ARROW_DOWN)
                tryAndRetryFillByXpath(driverinstance, '//input[contains(@id, "synonym-typeahead-text-field")]', Keys.RETURN)
                tryAndRetryFillByXpath(driverinstance, '//input[contains(@id, "location-typeahead-text-field")]', str(ville))
                tryAndRetryFillByXpath(driverinstance, '//input[contains(@id, "location-typeahead-text-field")]', Keys.ARROW_DOWN)
                tryAndRetryFillByXpath(driverinstance, '//input[contains(@id, "location-typeahead-text-field")]', Keys.RETURN)
                tryAndRetryFillByXpath(driverinstance, '//input[contains(@id, "location-typeahead-text-field")]', Keys.RETURN)
                waitloading(3, driverinstance)
            
            my_list = list()
            final_result = list()

            links = driverinstance.find_elements(By.XPATH,"//*[contains(@id, 'skip-link-target')]//div//main//aside//div//div//div//div//div//article//a")
                
            if len(links) == 0:
                print("Aucun lien trouvé.")
            else:
                for i in links:
                    step1 = (i.get_attribute('href'))
                    my_list.append(step1)
                    
                if len(my_list) > 5:
                    my_list = my_list[:5]
                print("----------------------------------"+str(len(my_list))+"-----------------------------------------")
                for j in my_list:
                    driverinstance.get(j)
                    waitloading(2, driverinstance)
                    date_offre = nows.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

                    myDict = {}
                    myDict["date"] = date_offre
                    myDict["url"] = str(j)
                    myDict["titre"]  = remove_tags(getinnertextXpath(driverinstance, "//body//h1"))


                    myDict["contrat"] = remove_tags(getinnertextXpath(driverinstance, "//*[contains(@data-cy, 'info-contract')]//div//span"))
                    myDict["ville"] =  remove_tags(getinnertextXpath(driverinstance, "//a[contains(@data-cy, 'info-location-link')]"))
                    
                    myDict["salary"] = ""
                    myDict["experience"] = ""
                    myDict["metier"] = ""
                    myDict["statut"] = ""
                    myDict["secteur"] = ""
                    myDict["cats"] = lieu_tres_precis_path
                    myDict["places"] = categories_path
                    myDict["compagny"] = ""
                    myDict["postTime"] = ""

                    driverinstance.switch_to.frame(driverinstance.find_element(By.XPATH, "//iframe"))
                    myDict["description"] = remove_tags(getinnertextXpath(driverinstance, "//body")).encode('unicode-escape').decode('utf-8')
                    

                    
                    name_e = str(date)+"-data.txt"
                    append_new_line(r''+name_e+'', str(myDict).encode('unicode-escape').decode('utf-8'))
                    final_result.append(myDict)
                                
                if len(final_result) > 0:
                    final_result = json.dumps(final_result)
                    final_result = (json.loads(final_result))


                    # Connexion au serveur MongoDB
                    client = pymongo.MongoClient("mongodb://192.168.1.174:27017")

                    # Vérification de l'existence de la base de données "TOUTE_OFFRE"
                    if "TOUTE_OFFRE" in client.list_database_names():
                        # Connexion à la base de données "TOUTE_OFFRE"
                        db = client["TOUTE_OFFRE"]
                    else:
                        # Création de la base de données "TOUTE_OFFRE"
                        db = client["TOUTE_OFFRE"]
                        print("La base de données 'TOUTE_OFFRE' a été créée")

                    # Connexion à la collection "2022-05-15" dans la base de données
                    collection = db[date]
                    collection.insert_many(final_result)
                else:
                    pass

        except NoSuchElementException:
            pass
        
        driverinstance.quit()



        dernier_etape_processus = date+".txt"
        with open(dernier_etape_processus, 'w') as file:
            file.write(str("8"))
    

    

def post_emploi_talent(date, etape_processus):

    if  etape_processus <= 7:
        
        option = FirefoxOptions()
        option.add_argument('--disable-notifications')
        option.add_argument("--mute-audio")
        option.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")
        driverinstance = webdriver.Firefox(options=option)

        initGoogle(driverinstance)
        driverinstance.get("https://emploi-talent.com/wp-admin")
        waitloading(1, driverinstance)
        tryAndRetryFillByXpath(driverinstance, '//input[contains(@id, "user_login")]', str('sauvegarde.pmgroupefrance@gmail.com'))
        tryAndRetryFillByXpath(driverinstance, '//input[contains(@id, "user_pass")]', str('63t7aK6nTo5LNEW'))
        tryAndRetryClickXpath(driverinstance, '//input[contains(@id, "wp-submit")]')
        waitloading(2, driverinstance)

        client = pymongo.MongoClient("mongodb://192.168.1.174:27017")
        db = client["TOUTE_OFFRE"]  
        collection = db[date]
        query = {}
        cursor = collection.find(query)
        results = list(cursor)
        json_data = json.dumps(results)
        for item in json_data:
            driverinstance.get("https://emploi-talent.com/wp-admin/post-new.php?post_type=job_listing")
            waitloading(2, driverinstance)
            recaptcha(driverinstance, '//button[contains(@aria-label, "Fermez la boite ")]')
            waitloading(0.5, driverinstance)
            categories = item["cats"]

            # Divisez la chaîne "categories" en trois parties en utilisant le délimiteur "/"
            # et affectez-les à des variables distinctes
            mainCat = str(categories.split('/')[0])
            secondaryCat = str(categories.split('/')[1])
            preciseCat = str(categories.split('/')[2])




def lire_ligne_precise():

    index = int(input("Entrez le numéro de la ligne à lire : "))

    df = pd.read_excel('./Populations.xlsx')
    # Vérifier si le numéro spécifié est valide
    if index < 0 or index >= len(df):
        print("Index invalide. Veuillez choisir un index valide.")
        return
    
    # Lire les colonnes spécifiées pour la ligne précise
    colonnes_demandees = ['Département / GV', 'Profession 1', 'Profession 2', 'Profession 3', 'Catégories', 'Lieu Très Précis']
    ligne_precise = df.loc[index, colonnes_demandees]

    # Afficher les valeurs lues
    print("Ligne précise (Index {}):".format(index))
    print(ligne_precise)


def lire_intervalle_tableau():
    # Ici, vous pouvez implémenter le code pour lire un intervalle de lignes dans le tableau
    # par exemple, en demandant à l'utilisateur de saisir un début et une fin d'index et en affichant les lignes correspondantes.
    print('"')

def lire_date_commune_precise():
    J = str(input("Entrez le jour voulu c'est-à-dire 09 ou 23 un jour en chiffre: "))
    M = str(input("Entrez le mois voulu dans le format suivant de 01 à 12, par exemple pour janvier '01': "))
    date = str('2022-'+M+'-'+J+'')
    print('---------------------------------------2022-'+M+'-'+J+'-------------------------------------------------------------------------')
    #subprocess.call(['curl', '-L', 'https://docs.google.com/spreadsheets/d/1a9wabH5oSOuzv6fQcR2wkETQu3M5OybyLDH7cPXxT_4/export?gid=0&format=xlsx', '-o', './Populations.xlsx'])
    dernier_etape_processus = date+".txt"
    try:
        with open(dernier_etape_processus, 'r') as file:
            etape_processus = str(file.read())
    except FileNotFoundError:
        etape_processus = 0

    df = pd.read_excel('./Populations.xlsx')
    colonne_date_post = df['Date de Post']
    condition = colonne_date_post.astype(str).str.startswith('2022-' + M + '-' + J)
    nouveau_dataframe = df[condition][['Département / GV', 'Profession 1', 'Profession 2', 'Profession 3', 'Catégories', 'Lieu Très Précis']]
    print(nouveau_dataframe)

    json_data = nouveau_dataframe.to_json(orient='records', force_ascii=False)
            
    json_data = json.loads(json_data)
    for item in json_data:
        # RES

        scrap_site_saveAnnonceIndeed(item['Profession 1'], item['Département / GV'], item['Catégories'], item['Lieu Très Précis'], date , int(etape_processus))
        scrap_site_saveAnnonceAPEC(item['Profession 1'], item['Département / GV'], item['Catégories'], item['Lieu Très Précis'], date , int(etape_processus))

        scrap_site_JobUp(item['Profession 1'], item['Département / GV'], item['Catégories'], item['Lieu Très Précis'], date , int(etape_processus))
        
        scrap_site_LINKEDIN(item['Profession 1'], item['Département / GV'], item['Catégories'], item['Lieu Très Précis'], date , int(etape_processus))

        scrap_site_saveAnnoncePE(item['Profession 1'], item['Département / GV'], item['Catégories'], item['Lieu Très Précis'], date , int(etape_processus))

        scrap_site_saveAnnonceHelloWork(item['Profession 1'], item['Département / GV'], item['Catégories'], item['Lieu Très Précis'], date , int(etape_processus))

    """           """
    post_emploi_talent(date , int(etape_processus))
    
    with open(dernier_etape_processus, 'w') as file:
        file.write(str("0"))

    
def publish():

    print("\n                   Bienvenue ! Que souhaitez-vous faire ?\n")
    print("1. Lire une seule ligne précise du tableau ( ex : juste ligne 323 )\n")
    print("2. Lire un intervalle de lignes dans le tableau ex : de 100 a 560 \n")
    print("3. Lire les données correspondant à une date précise ex : 15/02/2023\n")

    choix = int(input("Entrez le numéro de votre choix (1/2/3) : "))

    if choix == 1:
        lire_ligne_precise()
    elif choix == 2:
        lire_intervalle_tableau()
    elif choix == 3:
        lire_date_commune_precise()
    else:
        print("Choix invalide. Veuillez choisir une option valide (1/2/3).")






# Connexion au serveur MongoDB

publish() 



"""input('a1111111111111111')
driverinstance.switch_to.frame(driverinstance.find_element(By.XPATH, "//iframe"))
textInMail = remove_tags(getinnertextXpath(driverinstance, "//body"))
input(textInMail)"""


""""while True:
    try:
        publish()
        break
    except Exception as e:
        print("Une erreur s'est produite :", str(e))
        print("Redémarrage du script dans 5 secondes...")
        time.sleep(360)"""
 