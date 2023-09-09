
from cgi import test
import email
from lib2to3.pgen2 import driver
import linecache
import random
from typing_extensions import Self
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
import html2text
from datetime import datetime
from os.path import exists
# pour colorer les prints
from colorama import Fore
from colorama import Style
from urllib.parse import ParseResult, urlparse
from dateutil.relativedelta import relativedelta
import datetime
import requests, socket
from urllib3.connection import HTTPConnection

HTTPConnection.default_socket_options = ( 
    HTTPConnection.default_socket_options + [
    (socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000), #1MB in byte
    (socket.SOL_SOCKET, socket.SO_RCVBUF, 1000000)
])

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

from googletrans import Translator
translator = Translator()
import html
import pathlib
from urlextract import URLExtract
extractor = URLExtract()
from slugify import slugify


from ast import literal_eval

import os
sys.setrecursionlimit(10000)




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


class Spoofer(object):

    def __init__(self, country_id=['FR'], rand=True, anonym=True):
        self.country_id = country_id
        self.rand = rand
        self.anonym = anonym
        self.userAgent, self.ip = self.get()

    def get(self):
        ua = UserAgent()
        proxy = FreeProxy(country_id=self.country_id, rand=self.rand, anonym=self.anonym).get()
        ip = proxy.split("://")[1]
        return ua.random, ip


class DriverOptions(object):

    def __init__(self):

        self.options = Options()
        
        self.options.binary_location = "/usr/bin/google-chrome"
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--start-fullscreen')
        self.options.add_argument('--single-process')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument("--incognito")
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_argument("disable-infobars")

        self.helperSpoofer = Spoofer()

        self.options.add_argument('user-agent={}'.format(self.helperSpoofer.userAgent))
        self.options.add_argument('--proxy-server=%s' % self.helperSpoofer.ip)


class WebDriver(DriverOptions):

    def __init__(self, path=''):
        DriverOptions.__init__(self)
        self.driver_instance = self.get_driver()

    def get_driver(self):

        print("""
        IP:{}
        UserAgent: {}
        """.format(self.helperSpoofer.ip, self.helperSpoofer.userAgent))

        PROXY = self.helperSpoofer.ip
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy":PROXY,
            "ftpProxy":PROXY,
            "sslProxy":PROXY,
            "noProxy":None,
            "proxyType":"MANUAL",
            "autodetect":False
        }
        webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True

        path = os.path.join(os.getcwd(), '/home/ds/env/selenium/2023/chromedriver_linux64/chromedriver')

        driver = webdriver.Chrome(executable_path=path, options=self.options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source":
                "const newProto = navigator.__proto__;"
                "delete newProto.webdriver;"
                "navigator.__proto__ = newProto;"
        })

        return driver

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
        time.sleep(3)
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

def post_commet(driverinstance, link, title):
    if check_exists_by_xpath(driverinstance, '//form[contains(@id, "comment")]//textarea[contains(@id, "comment")]') == 0:
        try:
            tryAndRetryClickXpath(driverinstance, '//form[contains(@id, "comment")]//textarea[contains(@id, "comment")]')
            tryAndRetryFillByXpath(driverinstance, '//form[contains(@id, "comment")]//textarea[contains(@id, "comment")]', str('Je tenais à prendre un moment pour vous féliciter chaleureusement pour votre article inspirant et captivant En signe de gratitude pour votre excellent travail, Préparez-vous à augmenter votre chiffre d\'affaires jusqu\'à 50% grâce à une présence en ligne optimale ! Adoptez dès maintenant le meilleur hébergeur avec un nom de domaine gratuit et propulsez votre entreprise vers des sommets de succès inégalés. Ne manquez pas cette opportunité inestimable : agissez dès maintenant pour atteindre le succès absolu en ligne !'))
        except NoSuchElementException:
            pass
    if check_exists_by_xpath(driverinstance, '//form[contains(@id, "comment")]//input[contains(@id, "email")]') == 0:
        try:
            tryAndRetryFillByXpath(driverinstance, '//form[contains(@id, "comment")]//input[contains(@id, "email")]', str('contact@azienda-solution.com'))
        except NoSuchElementException:
            pass
    if check_exists_by_xpath(driverinstance, '//form[contains(@id, "comment")]//input[contains(@id, "author")]') == 0:
        try:
            tryAndRetryFillByXpath(driverinstance, '//form[contains(@id, "comment")]//input[contains(@id, "author")]', str('Débloquez votre potentiel'))
        except NoSuchElementException:
            pass
    if check_exists_by_xpath(driverinstance, '//form[contains(@id, "comment")]//input[contains(@id, "url")]') == 0:
        try:
            driverinstance.find_element(By.XPATH, '//form[contains(@id, "comment")]//input[contains(@id, "url")]').send_keys("https://tinyurl.com/hostinger-host")
        except NoSuchElementException:
            pass
    if check_exists_by_xpath(driverinstance, '//form[contains(@id, "comment")]//input[contains(@id, "submit")]') == 0:
        tryAndRetryClickXpath(driverinstance, '//form[contains(@id, "comment")]//input[contains(@id, "submit")]')
        
    if check_exists_by_xpath(driverinstance, '//form[contains(@id, "comment")]//button[contains(@id, "submit")]') == 0:
        tryAndRetryClickXpath(driverinstance, '//form[contains(@id, "comment")]//button[contains(@id, "submit")]')
    append_new_line(r'wordpress_website_done.txt', link)
    
def publish():
    option = FirefoxOptions()
    option.add_argument('--disable-notifications')
    option.add_argument("--mute-audio")
    option.add_argument("--headless")
    option.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")
    word_file = r"/opt/lampp/htdocs/avis-review.com/scrap/B/words_alpha.txt"
    WORDSSSS = open(word_file).read().splitlines()
    driverinstance = webdriver.Firefox(options=option)
    count_WORDS= (len(WORDSSSS))
    index_google = 1#final_result[random.randint(0, 8)]
    driverinstance.get("https://google.com")
    time.sleep(5)
    tryAndRetryClickXpath(driverinstance, '//button[contains(@id, "L2AGLb")]')
    time.sleep(5)
        
    for item in range(1, 8000):
        my_list = list()
        driverinstance.get("https://google.com")
        WORDS = str(WORDSSSS[int(random.randint(8, count_WORDS))])
        print(WORDS)
        #WORDS = "zeru ca .pdf"
        title = linecache.getline(r"/opt/lampp/htdocs/avis-review.com/scrap/all_link_sitemap.txt", item)
        link = linecache.getline(r"/opt/lampp/htdocs/avis-review.com/scrap/all_link_sitemap.txt", item)
        append_new_line(r'all_link_googlebot_done.txt', str(title))
        
        if "https://azienda-solution.com/" in title:
            title = title
        else:
            title = WORDS
        if "/wp-content/"  in title  or "listivotheme"  in title or "data:image"  in title or "/listivo_template/"  in title or "/wp-admin/"  in title:
            title = WORDS            
        title = title.replace('https://azienda-solution.com/avis/', '').replace('https://azienda-solution.com/review/', '').replace('https://azienda-solution.com/category/', '').replace('https://azienda-solution.com/tag/', '').replace('https://', '').replace('/', '').replace('.fr', '')
        
        title = re.sub(r'[^ \nA-Za-z0-9À-ÖØ-öø-ÿЀ-ӿ/]+', ' ', WORDS)
        #title = re.sub(r'[^ \nA-Za-z0-9À-ÖØ-öø-ÿЀ-ӿ/]+', ' ', title)
        
        try:
            driverinstance.find_element(By.XPATH, '//textarea[contains(@maxlength, "2048")]').send_keys(title)
        except NoSuchElementException:
            driverinstance.find_element(By.XPATH, '//input[contains(@maxlength, "2048")]').send_keys(title)
        #tryAndRetryFillByXpath(driverinstance, '//input[contains(@maxlength, "")]', title)
        
        actions = ActionChains(driverinstance)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(5)
        google_url = (driverinstance.current_url)
        google_url = google_url.replace('search?q=', 'search?num=80&q=')
        driverinstance.get(google_url)
        links = driverinstance.find_elements(By.XPATH,"//div[contains(@data-snhf, '0')]//a")
        #links = driverinstance.find_element_by_xpath("//div[contains(@data-, "")]//a")
        for i in links:
            step1 = (i.get_attribute('href'))
            __parsed_uri = urlparse(step1)
            __result = '{uri.scheme}://{uri.netloc}/'.format(uri=__parsed_uri)
            __hostname = __result
            #if "translate.g" in step1 or search_array(list_search, __hostname) == 11 or "translate.google" in step1 or ".pdf" in step1 or ".docx" in step1 or ".doc" in step1 or ".jpeg" in step1 or ".webp" in step1 or ".rar" in step1 or "wikipedia." in step1 or "dictionnaire" in step1 or "dictionnaire." in step1 or "faeebook." in step1 or "tikok." in step1 or "/download/" in step1:
            EXCLUDED_KEYWORDS = ["translate.g", "translate.google", ".pdf", ".docx", ".doc", ".jpeg", ".webp", ".rar", "wikipedia.", "dictionnaire", "dictionnaire.", "facebook.", "tikok.", "/download/", "/apt/", "apt/", ".txt", "amazon.", "adobe.", ".lingue", "-francais", "/traduction/", "/dictionary", "/traduction/", ".ebay", ".fnac", "/traduction/", "definitions", "/definition", "/wiki", "wiktionary", "dictionary.", "twitch.", "encyclo", ".youtube", "?pdf", "pdf=", ".html", ".php", ".pptx", "?path", "path=", "/path", ".pps", "google.", ".google.", ".tiktok", "search.do?recordID", ".pensoft.net", ".virginialiving.", "/PDF/", "/object/", "PDF/", ".mnhn.fr", "gtgrecords.net", "komitid.fr", "/translate/", "linkedin.", ".parismuseescollections.", ".instagram"]
            if any(keyword in str(step1) for keyword in EXCLUDED_KEYWORDS):
                pass
            else:
                my_list.append(step1)
        count = len(my_list)
        print(count)
        
        for j in my_list:
            print(title)
            print(j)
            if get_website_status(j) == "200":
                try:
                    driverinstance.get(j)
                    time.sleep(9)
                    # from urlparse import urlparse  # Python 2
                    parsed_uri = urlparse(j)
                    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                    hostname = result
                    if get_website_status(hostname+"wp-admin/") == "200":
                        driverinstance.get(hostname+"wp-admin/")
                        time.sleep(5)
                        if "wp-login" in driverinstance.page_source or check_exists_by_xpath(driverinstance, '//*[contains(@id, "login")]') == 0:
                            driverinstance.get(j)
                            time.sleep(5)
                            if check_exists_by_xpath(driverinstance, '//input[contains(@id, "author")]') == 0:
                                post_commet(driverinstance, hostname, title)
                            else:
                                driverinstance.get(hostname+"?s=+&post_type=post")
                                time.sleep(5)
                                
                                
                                my_list__ = list()
                                post_link = driverinstance.find_elements(By.XPATH,'//a[contains(@rel, "bookmark")]')
                                for i__ in post_link:
                                    step2 = (i__.get_attribute('href'))
                                    my_list__.append(step2)
                                    
                                longueur_liste = len(my_list__)
                                longueur_liste = longueur_liste - 1

                                for __i in range(longueur_liste):
                                    if __i < longueur_liste:
                                        yyy = int(random.randint(0, longueur_liste))
                                        post_link = my_list__[yyy]
                                        print(str(post_link))
                                        print("___________________________________")
                                        if get_website_status(post_link) == "200":
                                            driverinstance.get(post_link)
                                            time.sleep(5)
                                            if check_exists_by_xpath(driverinstance, '//input[contains(@id, "author")]') == 0:
                                                time.sleep(5)
                                                post_commet(driverinstance, post_link, title)
                                    else:
                                        print("L'index", i, "n'existe pas dans la liste")
                                        
                        else:
                            pass
                    else:
                        pass
                    
                except NoSuchElementException:
                    pass
            else:
                pass
                
        append_new_line(r'all_link_googlebot_done.txt', str(link))
    driverinstance.close()
        
        
list_search = list()
list_search = ["facebook.com", "reddit","wikipedia"]

final_result = list()
final_result = ["fr", "com","cn","es","ca","ru","de",".com.hk", ".co.uk"]

#browser()
#postbrowser()
def get_website_status(url):
    """ 
    retry_count = 2 # Nombre de tentatives de vérification en cas d'échec
    retry_interval = 3 # Intervalle entre chaque tentative de vérification (en secondes)
    status_code = 404
    
    for i in range(retry_count + 1):
        try:
            response = requests.get(url, verify=False, timeout=120)
            status_code = response.status_code
        except requests.exceptions.ConnectionError:
            try:
                time.sleep(3)
                response = requests.get(url, verify=False, timeout=120)
                status_code = response.status_code
            except Exception as e:
                print(e)
        
        if status_code >= 200 and status_code < 300:
            print("L'URL", url, "a renvoyé une réponse valide:", status_code)
            result = "200"
        elif i == retry_count:
            result = "NONE"
            print("L'URL", url, "a échoué après", retry_count, "tentatives")
        else:
            result = "NONE"
            print("L'URL", url, "a renvoyé une réponse inattendue:", status_code)
            print("Reprise de la vérification dans", retry_interval, "secondes...")
            time.sleep(retry_interval)
    return str(result)""" 
    result = "NONE"
    # handle connection errors
    try:
        # open a connection to the server with a timeout
        with urlopen(url, timeout=5) as connection:
            # get the response code, e.g. 200
            code = connection.getcode()
            result = (code)
            result = "200"
    except HTTPError as e:
        result = "NONE"
    except URLError as e:
        result = "NONE"
    except:
        result = "NONE"
    print(result)
    parsed_uri8888 = urlparse(url)
    result8888 = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri8888)
    hostname8888 = result8888
    list_search.append(hostname8888)
    return str(result)




while True:
    try:
        publish()
        break
    except Exception as e:
        print("Une erreur s'est produite :", str(e))
        print("Redémarrage du script dans 5 secondes...")
        time.sleep(5)  # Attendre 5 secondes avant de redémarrer

#get_website_status("")
