from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import InvalidSelectorException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from os.path import exists
# pour colorer les prints
from colorama import Fore
from colorama import Style
from urllib.parse import ParseResult, urlparse

# pour colorer les prints
import colorama
import os
import os.path
import re
import time
import json

colorama.init() 
listeDeLiensNonClean = list()
listeDeLiensClean = list()

offresIndeed = list()

def scroll_function(i):
    height = i * 1000
    time.sleep(1.3)
    driver.execute_script("window.scrollTo("+ str(height) +", "+ str(height) +")")
    time.sleep(1.3)
    
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(description):
    return TAG_RE.sub(' ', description)

def recapcha():
    try:
        driver.find_element(By.XPATH,"//a[contains(@onclick,'closeGoogleOnlyModal')]").click()
        recapcha = driver.find_element(By.ID,"popover-background").click()
        recapcha = driver.find_element(By.ID,"popover-background").click()
    except NoSuchElementException:  #spelling error making this code not work as expected
        pass

driver = webdriver.Firefox()
driver.get("https://www.google.com")

cookieGoogle = driver.find_element(By.ID,'L2AGLb').click()
if cookieGoogle:
    print("GOOGLE a changé l'id recupere le nouveau")
else:
    print("Init Google...")
    #On valide les cookies
    urlParent = input("Entrer le lien de la page indeed sans le cookie &vjk ^^:\n")
    urlParent = urlParent + "&limit=100&sort=date&filter=0"
    # parsing de l'url pour récupérer le titre du job et la ville du job a scrapé
    urlParse = urlParent.split("?")
    urlParse = urlParse[1].split("&")
    urlTitreJob = urlParse[0].split("=")
    urlVilleJob = urlParse[1].split("=")
    urlTitreJob = urlTitreJob[1]
    urlVilleJob = urlVilleJob[1]
    urlFinal = urlTitreJob + "-" + urlVilleJob

    driver.get(urlParent)
    time.sleep(3)
    #On attend la page charge
    print("On attend le site charge ...")

    try:
        onetrust = driver.find_element(By.XPATH,'//*[@id="onetrust-reject-all-handler"]').click()
    except NoSuchElementException:
        pass
    time.sleep(1)
    print("Cookie validé")

    links = driver.find_elements(By.CLASS_NAME,'jcs-JobTitle')
    nombreDeLiens = len(links)
    if (nombreDeLiens < 4):
        print(urlParent)
        recapcha()
        time.sleep(1)
        links = driver.find_elements(By.XPATH,'/html/body/table/tbody/tr/td/table/tbody/tr/td/div/div/a')
        nombreDeLiens = len(links)
    # commenté cette ligne elif si vous voulez scrapper plus de 10jobs
    # elif (nombreDeLiens > 15):
    #     nombreDeLiens = 15
    #     print(nombreDeLiens)
    # else:
    #     print(nombreDeLiens)
    
    comptePour12Liens = 0
    while comptePour12Liens < nombreDeLiens:
        link = (links[comptePour12Liens].get_attribute('href'))
        listeDeLiensNonClean.append(link)
        comptePour12Liens = comptePour12Liens + 1

    print(listeDeLiensNonClean)
    print(len(listeDeLiensNonClean))
    
    # on nettoye les 2 premiers liens de la base de donnée car il ne sont pas utiles
    cleanLinks = []
    compteurLink = 2

    while compteurLink < nombreDeLiens:
        listeDeLiensClean.append(listeDeLiensNonClean[compteurLink])
        compteurLink = compteurLink +1
    
    print(Fore.RED + "problem occured with xpath...")
    print(Style.RESET_ALL)
    if (listeDeLiensClean == 0):
        try:
            onetrust = driver.find_element(By.XPATH,'//*[@id="onetrust-reject-all-handler"]').click()
        except NoSuchElementException:
            pass
        time.sleep(1)
        print("Cookie validé")

        links = driver.find_elements(By.CLASS_NAME,'jcs-JobTitle')
        nombreDeLiens = len(links)
        if (nombreDeLiens < 4):
            print(urlParent)
            recapcha()
            time.sleep(1)
            links = driver.find_elements(By.XPATH,'/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[4]/div/ul/li/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[1]/h2')
            nombreDeLiens = len(links)
        # commenté cette ligne elif si vous voulez scrapper plus de 10jobs
        # elif (nombreDeLiens > 15):
        #     nombreDeLiens = 15
        #     print(nombreDeLiens)
        # else:
        #     print(nombreDeLiens)
        
        comptePour12Liens = 0
        while comptePour12Liens < nombreDeLiens:
            link = (links[comptePour12Liens].get_attribute('href'))
            listeDeLiensNonClean.append(link)
            comptePour12Liens = comptePour12Liens + 1

        print(listeDeLiensNonClean)
        print(len(listeDeLiensNonClean))
        
        # on nettoye les 2 premiers liens de la base de donnée car il ne sont pas utiles
        cleanLinks = []
        compteurLink = 2

        while compteurLink < nombreDeLiens:
            listeDeLiensClean.append(listeDeLiensNonClean[compteurLink])
            compteurLink = compteurLink +1

    print(len(listeDeLiensClean))
    # print(listeDeLiensClean)

    input("//////////// RESULTAT A L'ECRAN \n")

    # mettre nombre d'offre desire à 25 pour récuper le max de lien
    # offresLiens = 0
    # nombreDoffresDesire = 10

    for scrappingUrl in listeDeLiensClean:
        # while offresLiens <= nombreDoffresDesire:
        driver.get(scrappingUrl)
        print('waiting 2sec...')
        time.sleep(2)
        recapcha()

        # stockage de la date actuelle
        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        print(date)

        # récupération de l'url
        url = scrappingUrl
        print(url)

        # récupération du titre
        titre = driver.find_elements(By.XPATH,'//div[contains(@class, "jobsearch-JobInfoHeader-title-container")]//h1[contains(@class, "jobsearch-JobInfoHeader-title")]')
        for titreLien in titre: 
            titre = (titreLien.get_attribute('innerHTML'))
        print(titre)
        metier = titre

        # récupération de la ville
        try:
            ville = driver.find_element(By.XPATH,'//*[@id="viewJobSSRRoot"]/div[2]/div/div[3]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div')
            ville = ville.text
        except InvalidSelectorException:
            try:
                ville = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div[3]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div')
                ville = ville.text
            except InvalidSelectorException:
                ville = driver.find_element(By.CLASS_NAME,'.icl-u-textColor--secondary > div:nth-child(2) > div:nth-child(1)')
                ville = ville.text
        except NoSuchElementException:  #spelling error making this code not work as expected
            try:
                ville = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div[3]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div')
                ville = ville.text
            except InvalidSelectorException:
                ville = driver.find_element(By.CLASS_NAME,'.icl-u-textColor--secondary > div:nth-child(2) > div:nth-child(1)')
                ville = ville.text
            except NoSuchElementException:
                try:
                    ville = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[3]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]')
                    ville = ville.text
                except InvalidSelectorException:
                    ville = driver.find_element(By.CLASS_NAME,'.icl-u-textColor--secondary > div:nth-child(2) > div:nth-child(1)')
                    ville = ville.text
                except NoSuchElementException:
                    try:
                        ville = driver.find_element(By.CLASS_NAME,'.icl-u-textColor--secondary > div:nth-child(2) > div:nth-child(1)')
                        ville = ville.text
                    except NoSuchElementException:
                        ville = 'France'
                        pass
                    except InvalidSelectorException:
                        ville = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div[3]/div/div/div[1]/div[1]/div[3]/div[1]/div[2]/div/div/div/div[2]/div')
                        ville = ville.text
                        
        print(Fore.GREEN + ville + Style.RESET_ALL)

        # récupération de la description
        try:
            description = driver.find_element(By.XPATH,'//div[contains(@id, "jobDescriptionText")]')
            description = description.text
        except NoSuchElementException:  #spelling error making this code not work as expected
            try:
                description = driver.find_element(By.ID,'jobDescriptionText')
                description = description.text
            except NoSuchElementException:
                description = "contactez l'employeur"
                pass
        # else:
        #     

        print(description)
        time.sleep(1)

        # récupération du salaire
        try:
            salary = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div[2]/div[1]/div/span[1]')
            salary = salary.text
        except NoSuchElementException:
            salary = 'A définir'
            print(Fore.RED + 'bug xpath salary')
            print(Style.RESET_ALL)
            pass
        print(salary)

        # récupération du type de contrat
        try:
            contrat = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div[2]/div[1]/div/span[2]')
            contrat = contrat.text
        except NoSuchElementException:  #spelling error making this code not work as expected
            contrat = "CDI"
            pass
        print(contrat)
        statut = contrat

        # récupération du secteur
        try:
            secteur = titre.text.split()[0]
        except AttributeError:
            secteur = titre
        else:
            secteur = titre.text.split()[0]

        experience = "Tous niveaux d'expérience acceptés"


        myDict = {}
        myDict["date"] = date
        myDict["url"] = url
        myDict["titre"] = titre
        myDict["ville"] = ville
        myDict["contrat"] = contrat
        myDict["description"] = description
        myDict["salary"] = salary
        myDict["metier"] = metier
        myDict["statut"] = statut
        myDict["secteur"] = secteur
        myDict["experience"] = experience
        offresIndeed.append(myDict)
        # offresLiens = offresLiens + 1

with open(f"stockageOffreIndeed/{urlFinal}.json", "wb") as writeJSON:
   jsStr = json.dumps(offresIndeed)
   # the decode() needed because we need to convert it to binary
   writeJSON.write(jsStr.encode('utf-8')) 
print ('end')