# Fonction principalmement utilisé lors du début d'une instance gecko driver pour cliquer et remplier des champs par exemple
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import InvalidSelectorException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert 
from selenium.webdriver.chrome.service import Service

from datetime import datetime

import importlib.util
from importlib.abc import Finder
import sys

try:
    from headerSeleniumPoster import *
except ModuleNotFoundError:
    importlib.util.module_for_loader

import re
import time
import json
import random
import colorama
from colorama import Fore
from colorama import Style

colorama.init()

# fonction pour créer un dictionnaire et retourner ses valeurs
def make_a_dict_of_values(date,url,titre,ville,contrat,description,salary,metier,statut,secteur,experience):
    myDict = {
    "date" : date, 
    "url" : url, 
    "titre" : titre, 
    "ville" : ville, 
    "contrat" : contrat, 
    "description" : description, 
    "salary" : salary,
    "metier" : metier,
    "statut" : statut,
    "secteur" : secteur,
    "experience" : experience }
    return myDict

# fonction pour créer un dictionnaire et retourner ses valeurs
def make_a_dict_of_valuesV2(date,url,titre,ville,contrat,description,salary,statut,secteur,experience,metier,lieux,categorie):
    myDict = {
    "date" : date, 
    "url" : url, 
    "titre" : titre, 
    "ville" : ville, 
    "contrat" : contrat, 
    "description" : description, 
    "salary" : salary,
    "metier" : metier,
    "statut" : statut,
    "secteur" : secteur,
    "experience" : experience,
    "lieux": lieux,
    "categorie": categorie}
    return myDict
    
def timeSleeper():
    randomTime = random.randint(1,3)
    print(Fore.BLUE + str(randomTime) + "sec en attente via la fonction timeSleeper; retirer la pour aller plus vite !!attention si vous faites ca vous avez des risques de ban ip, activez votre VPN")
    print(Style.RESET_ALL)
    time.sleep(randomTime)

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(description):
    return TAG_RE.sub(' ', description)

def recapcha(argDriver):
    try:
        argDriver.find_element(By.XPATH,"//a[contains(@onclick,'closeGoogleOnlyModal')]").click()
        recapcha = argDriver.find_element(By.ID,"popover-background").click()
        recapcha = argDriver.find_element(By.ID,"popover-background").click()
    except NoSuchElementException:  #spelling error making this code not work as expected
        pass