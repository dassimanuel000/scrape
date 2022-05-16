from calendar import c
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from datetime import datetime
from os.path import exists


# pour colorer les prints
from colorama import Fore
from colorama import Style
from urllib.parse import ParseResult, urlparse
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook

# pour colorer les prints
import colorama
import os
import os.path
import re
import time
import json
import random

colorama.init()
# stockage du path du script  
currentDir = os.path.abspath(os.getcwd())
currentDir = currentDir.replace('\\', '/')
print(currentDir)

def make_a_converted_list_job(date):
    listeDesJobsDeCetteDate = list(df1[df1['Date de Post'] == f'{date}']['Profession 1'])
    return listeDesJobsDeCetteDate

def make_a_converted_list_departement(date):
    listeDesDptmntsDeCetteDate = list(df1[df1['Date de Post'] == f'{date}']['Département / GV'])
    return listeDesDptmntsDeCetteDate

def scroll_function(i):
    height = i * 1000
    time.sleep(1.3)
    driver.execute_script("window.scrollTo("+ str(height) +", "+ str(height) +")")
    time.sleep(1.3)

def timeSleeper():
    randomTime = random.randint(1,3)
    print(Fore.BLUE + str(randomTime) + "sec en attente via la fonction timeSleeper; retirer la pour aller plus vite !!attention si vous faites ca vous avez des risques de ban ip, activez votre VPN")
    print(Style.RESET_ALL)
    time.sleep(randomTime)

    
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

# connection à l'excel préalablement téléchargé
df = pd.read_excel (r'Populations.xlsx', parse_dates=['Date de Post'])
# récupération des 7 premières colonnes verticales
df1 = df.iloc[: , :7] 

# récupération de la date dans l'excel permettant la création des listes de dates désirées
J = input("Tapez le jour désiré de 01 à 31: \n")
M = input("Tapez le mois désiré de 01 à 12: \n")
date = f'2022-{M}-{J} 00:00:00'
# Dossier à creer
directory = "stockageOffreIndeed" + J + M

# mode
mode = 0o666

# Path
path = os.path.join(currentDir, directory)

# Create the directory
try:
    os.mkdir(path, mode)
    print("Directory '% s' created" % directory)
except FileExistsError:
    print('Dossier déja existant')

listeJob = make_a_converted_list_job(date)
listeDepartement = make_a_converted_list_departement(date)
nombreDeBouclesListeDates = len(listeDepartement)
compteurBouclesListeDates = 0

print(listeJob)
print(listeDepartement)

while compteurBouclesListeDates < nombreDeBouclesListeDates:
    listeDeLiensNonClean = list()
    listeDeLiensClean = list()
    print(listeJob[compteurBouclesListeDates])
    goodListeJob = listeJob[compteurBouclesListeDates].split('/')
    print(goodListeJob)
    noSlashJob = goodListeJob[0]
    print(noSlashJob)

    goodListeDepartement = listeDepartement[compteurBouclesListeDates].replace(' / ', '/').replace(' /', '/').replace('/ ','/').split('/')
    noSlashDepartement = goodListeDepartement[0]
    goodSlashDepartement = noSlashDepartement.split(',')
    noVirguleDepartement = goodSlashDepartement[0]
    offresIndeed = list()

    driver = webdriver.Firefox(executable_path=r'C:\Python310\geckodriver.exe')
    driver.get("https://google.com/")

    cookieGoogle = driver.find_element(By.ID,'L2AGLb').click()
    try:
        driver.find_element(By.CLASS_NAME, 'h-captcha')
        input(Fore.BLUE + 'Captcha à résoudre veuillez le résoudre et tapez entrez pour continuer...')
        print(Style.RESET_ALL)
    except NoSuchElementException:
        print("No captcha")
    
    if cookieGoogle:
        print("GOOGLE a changé l'id recupere le nouveau")
    else:
        print("Init Google...")
        #On valide les cookies
        urlParent = 'https://fr.indeed.com/jobs?q='+noSlashJob+'&l='+ noVirguleDepartement
        urlParent = urlParent + "&fromage=14&limit=25&sort=date&filter=0"
        # parsing de l'url pour récupérer le titre du job et la ville du job a scrapé
        urlParse = urlParent.split("?")
        urlParse = urlParse[1].split("&")
        urlTitreJob = urlParse[0].split("=")
        urlVilleJob = urlParse[1].split("=")
        urlTitreJob = urlTitreJob[1]
        urlVilleJob = urlVilleJob[1]
        urlFinal = urlTitreJob + "--" + urlVilleJob
        print(urlFinal)
        forJson = str(compteurBouclesListeDates) + "--" + urlFinal
        # faire fonctionner un modulo qui affichera les lettres de l'alphabet
        # if(forJson >= 10):
        #     forJson = 
        print(forJson)
        driver.get(urlParent)
        timeSleeper()
        #On attend la page charge
        print("On attend le site charge ...")

        try:
            onetrust = driver.find_element(By.XPATH,'//*[@id="onetrust-reject-all-handler"]').click()
        except NoSuchElementException:
            pass
        timeSleeper()
        print("Cookie validé")

        links = driver.find_elements(By.CLASS_NAME,'jcs-JobTitle')
        nombreDeLiens = len(links)
        if (nombreDeLiens < 4):
            print(urlParent)
            recapcha()
            timeSleeper()
            links = driver.find_elements(By.XPATH,'/html/body/table/tbody/tr/td/table/tbody/tr/td/div/div/a')
            nombreDeLiens = len(links)
        # commenté cette ligne elif si vous voulez scrapper plus de 10jobs
        if (nombreDeLiens > 17):
            nombreDeLiens = 17
            print(nombreDeLiens)
        else:
            print(nombreDeLiens)
        
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
        
        
        if (listeDeLiensClean == 0):
            print(Fore.RED + "problem occured with xpath...")
            print(Style.RESET_ALL)
            try:
                onetrust = driver.find_element(By.XPATH,'//*[@id="onetrust-reject-all-handler"]').click()
            except NoSuchElementException:
                pass
            timeSleeper()
            print("Cookie validé")

            links = driver.find_elements(By.CLASS_NAME,'jcs-JobTitle')
            nombreDeLiens = len(links)
            if (nombreDeLiens < 4):
                print(urlParent)
                recapcha()
                timeSleeper()
                links = driver.find_elements(By.XPATH,'/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[4]/div/ul/li/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[1]/h2')
                nombreDeLiens = len(links)
            # commenté cette ligne elif si vous voulez scrapper plus de 10jobs
            elif (nombreDeLiens > 17):
                nombreDeLiens = 17
                print(nombreDeLiens)
            else:
                print(nombreDeLiens)
            
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

        # input d'attente facultatif
        # input("//////////// RESULTAT A L'ECRAN \n")

        # mettre nombre d'offre desire à 25 pour récuper le max de lien
        # offresLiens = 0
        # nombreDoffresDesire = 10

        for scrappingUrl in listeDeLiensClean:
            # while offresLiens <= nombreDoffresDesire:
            driver.get(scrappingUrl)
            print('waiting 2sec...')
            timeSleeper()
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
                if titre == '[]':
                    print(Fore.RED + 'titre bugged, stopping the loop')
                    titreLien[titre] = None
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

                    with open(f"{directory}/{forJson}.json", "wb") as writeJSON:
                        jsStr = json.dumps(offresIndeed)
                        # the decode() needed because we need to convert it to binary
                        writeJSON.write(jsStr.encode('utf-8')) 
                        print ('end')

                    print(Style.RESET_ALL)
                    break
            print(titre)
            metier = titre

            # récupération de la ville
            try:
                ville = driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[1]/div[2]/div/div/div/div[2]')
                ville = ville.text
            except NoSuchElementException:  #spelling error making this code not work as expected
                ville = "France"
            print(ville)

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
            timeSleeper()

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

    with open(f"{directory}/{forJson}.json", "wb") as writeJSON:
        jsStr = json.dumps(offresIndeed)
        # the decode() needed because we need to convert it to binary
        writeJSON.write(jsStr.encode('utf-8')) 
        print ('end')
    compteurBouclesListeDates = compteurBouclesListeDates +1
    print(Fore.YELLOW + str(compteurBouclesListeDates))
    print(Style.RESET_ALL)
    driver.quit()