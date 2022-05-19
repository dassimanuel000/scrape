from calendar import c
from tkinter import TRUE
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from datetime import datetime
from os.path import exists
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

# pour colorer les prints
import colorama
# pour colorer les prints
from colorama import Fore
from colorama import Style

#Stack tech
from subprocess import check_output
import requests
import urllib.request
from urllib.parse import ParseResult, urlparse
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook

import os
import os.path
import re
import time
import json
import random
from datetime import datetime


def loginTuc(driver):
    time.sleep(2)
    driver.get("https://trouver-un-candidat.com/wp-admin/")
    user_login_Element = driver.find_elements_by_xpath('//*[@id="user_login"]')
    time.sleep(1)
    for iuser_login_ in user_login_Element:
        nomuser_login_ = iuser_login_.send_keys("annoncetrouveruncandidat")
        print("user_login_ ADD")
    time.sleep(1)
    
    user_passElement = driver.find_elements_by_xpath('//*[@id="user_pass"]')
    time.sleep(1)
    time.sleep(1)
    for juser_pass in user_passElement:
        user_passElement.clear()
        n_user_pass = juser_pass.send_keys("(%)Sku&mv#35OewiC%")
        print("user_pass ADD")
    time.sleep(2)
    divs = driver.find_element_by_xpath('//*[@id="wp-submit"]')
    divs.click()
    time.sleep(2)
    login = TRUE

def poster(offresIndeed, driver):
    print('postage .........')
    time.sleep(2)
    loginTuc(driver)

    offresIndeed = json.dumps(offresIndeed)
    #json_raw= list_indeed.readlines()
    offresIndeed = json.loads(offresIndeed)
    for item_job in offresIndeed:
        driver.get("https://trouver-un-candidat.com/wp-admin/post-new.php?post_type=job_listing")
        time.sleep(2)
        try:
            time.sleep(2)
            
            divs = driver.find_element_by_xpath('//div[contains(@class, "components-modal__header-heading-container")]')
            parent_elem  = divs.find_element_by_xpath('//button[contains(@aria-label, "Fermez la boite de dialogue")]').click()
            time.sleep(1)
            print("yes popup")
        except NoSuchElementException:
            print("NO popup")
            pass

        try:
            driver.find_element_by_class_name('interface-interface-skeleton__body').click()
            time.sleep(1)
        except NoSuchElementException:
            pass

        try:
            titre = driver.find_element_by_class_name('editor-post-title__input')
            titre.send_keys(item_job['description'])
            titre.send_keys(Keys.ENTER)
            titre.send_keys(item_job['titre'])
            titre.send_keys(Keys.ENTER)
            #driver.execute_script("alert('11555555555');")
            time.sleep(1)
        except NoSuchElementException:
            pass

        #try:
        #driver.find_element(By.XPATH, '//p[contains(@contenteditable, "true")]').send_keys(item_job['description'])
        #except NoSuchElementException:
        #    pass

        try:
            driver.find_element(By.XPATH,'//*[@id="job_listing_metabox"]').click()
            time.sleep(1)
        except NoSuchElementException:
            pass
        try:                              
            _job_apply_type = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div[4]/div[1]/div[1]/form/div/div/div/div[3]/div[2]/div/div/div/div/div/div[1]/div[7]/div[2]/span/span[1]/span/span[2]').click()
            #_job_apply_type = driver.find_element(By.XPATH,'//li[contains(.,"URL externe")]').click()
            _job_apply_type.send_keys(Keys.DOWN)
            _job_apply_type.send_keys(Keys.DOWN)
            _job_apply_type.send_keys(Keys.ENTER)
            time.sleep(1)
        except NoSuchElementException:
            pass
        

#

offresIndeed= [{"date": "2022-05-19-16:31:26", "url": "https://fr.indeed.com/company/Ibis-Soissons/jobs/R%C3%A9ceptionniste-Tournante-41060b011901b9d5?fccid=0866ff638e94ba70&vjs=3", "titre": "R\u00e9ceptionniste tournante H/F", "ville": "02200 Soissons", "contrat": "- Temps partiel, CDD", "description": "Attentif aux autres et \u00e0 l\u2019environnement qui vous entoure : vous contribuez \u00e0 rendre le s\u00e9jour aussi irr\u00e9prochable qu\u2019inoubliable en apportant votre petite touche personnelle !\nTr\u00e8s \u00e0 l\u2019aise en fran\u00e7ais et en anglais\nVous assurez un accueil personnalis\u00e9 et chaleureux, le bien-\u00eatre des clients est toujours votre priorit\u00e9.\nVous faites le lien avec les diff\u00e9rents d\u00e9partements de l\u2019h\u00f4tel selon les demandes clients, vous \u00eates un \u201cfacilitateur\u201d reconnu au sein de l\u2019\u00e9tablissement.\nVous avez \u00e0 c\u0153ur d\u2019am\u00e9liorer continuellement la qualit\u00e9 des services de l\u2019h\u00f4tel, vos id\u00e9es sont les bienvenues !\nVous \u00eates garant de la fid\u00e9lisation du client, ils reviendront s\u00fbrement un peu pour vous.\nVous serez form\u00e9 au suivi financier des recettes, et \u00e0 la s\u00e9curit\u00e9 des biens et des personnes.\nLors du travail de nuit, vous \u00eates responsable des activit\u00e9s de l\u2019\u00e9tablissement en l\u2019absence de votre hi\u00e9rarchie : cl\u00f4ture h\u00f4teli\u00e8re, encaissement, et anticipation des besoins du lendemain.\nType d'emploi : Temps partiel, CDD\nDur\u00e9e du contrat : 3 mois\nNombre d'heures : 32 par semaine\nSalaire : 11,30\u20ac par heure\nHoraires :\nP\u00e9riodes de travail de 8 heures\nExp\u00e9rience:\nr\u00e9ceptionniste H/F: 1 an (Exig\u00e9)\nR\u00e9ception: 1 an (Optionnel)\nLangue:\nAnglais (Exig\u00e9)\nDate de d\u00e9but pr\u00e9vue : 27/06/2022", "salary": "11,30 \u20ac par heure", "metier": "R\u00e9ceptionniste tournante H/F", "statut": "- Temps partiel, CDD", "secteur": "R\u00e9ceptionniste tournante H/F", "experience": "Tous niveaux d'exp\u00e9rience accept\u00e9s"}, {"date": "2022-05-19-16:31:31", "url": "https://fr.indeed.com/company/SAS-LE-1920/jobs/R%C3%A9ceptionniste-110ddb5baae5b450?fccid=232341c208989769&vjs=3", "titre": "R\u00e9ceptionniste, veilleur de nuit H/F", "ville": "Saint-Quentin (02)", "contrat": "- CDI", "description": "Accueil des clients individuels et des groupes ; Gestion des r\u00e9servations, comptes clients et encaissements ; Pr\u00e9sentation des prestations de l\u2019h\u00f4tel et promotions des ventes additionnelles ; Coordination avec le service petits d\u00e9jeuners.\nAssurer le d\u00e9veloppement de l\u2019\u00e9tablissement ; travailler de fa\u00e7on autonome d\u2019apr\u00e8s des proc\u00e9dures pr\u00e9\u00e9tablies ; s\u2019adapter \u00e0 la diversit\u00e9 de la client\u00e8le ; parler deux langues minimums.\nType d'emploi : CDI\nSalaire : 1 600,00\u20ac \u00e0 1 800,00\u20ac par mois\nHoraires :\nDisponible le week-end\nTravail de nuit\nExp\u00e9rience:\nR\u00e9ception: 3 ans (Exig\u00e9)\nLangue:\nAnglais (Exig\u00e9)", "salary": "1 600 \u20ac - 1 800 \u20ac par mois", "metier": "R\u00e9ceptionniste, veilleur de nuit H/F", "statut": "- CDI", "secteur": "R\u00e9ceptionniste, veilleur de nuit H/F", "experience": "Tous niveaux d'exp\u00e9rience accept\u00e9s"}, {"date": "2022-05-19-16:31:38", "url": "https://fr.indeed.com/company/TERNOVEO/jobs/Standardiste-Accueil-a3176bacca3b37f3?fccid=78d62476f31a2989&vjs=3", "titre": "Standardiste et accueil H/F", "ville": "02100 Saint-Quentin", "contrat": "CDI", "description": "Rejoindre TERNOVEO, c\u2019est rejoindre un n\u00e9goce dynamique et visionnaire du Groupe Advitam, c\u2019est se donner l\u2019opportunit\u00e9 d\u2019\u00eatre acteur des mutations du monde agricole.\nEngag\u00e9es, volontaires, professionnelles, nos \u00e9quipes font preuve de souplesse et de r\u00e9activit\u00e9 afin d\u2019acc\u00e9l\u00e9rer la r\u00e9ussite de nos clients et de l\u2019entreprise.\nEn tant qu\u2019Activateur de progr\u00e8s, TERNOVEO s\u2019engage au quotidien pour proposer des pistes novatrices r\u00e9pondant aux attentes de ses clients agriculteurs et aux enjeux gouvernementaux, environnementaux et soci\u00e9taux.\nL\u2019innovation est au c\u0153ur de notre ADN !\nTERNOVEO, Innover pour se d\u00e9velopper, pour se diversifier, pour p\u00e9renniser.\nBas\u00e9 au si\u00e8ge \u00e0 St-Quentin (02), vous serez rattach\u00e9(e) \u00e0 la Direction Administrative et Financi\u00e8re, pour accueillir et renseigner les interlocuteurs, contribuer aux t\u00e2ches administratives, tout en facilitant le quotidien des collaborateurs, vous aurez pour mission les activit\u00e9s suivantes :\nMissions standard / accueil :\nAccueillir, renseigner et orienter les clients et visiteurs ;\nR\u00e9ceptionner, filtrer et transf\u00e9rer les appels t\u00e9l\u00e9phoniques entrants ;\nR\u00e9aliser la gestion du courrier (collecte, distribution, exp\u00e9dition) ;\nUtiliser les outils collaboratifs (planning partag\u00e9, web conf\u00e9rence).\nMissions administratives courantes :\nR\u00e9aliser des t\u00e2ches administratives et suivi de dossiers (r\u00e9daction de courriers, publipostage \u2026) ;\nSe charger de la r\u00e9servation des repas et des salles de r\u00e9unions selon les demandes des collaborateurs\nG\u00e9rer l\u2019approvisionnement et le stock des fournitures administratives (papeterie, \u2026) ;\nEtre le relais avec la Soci\u00e9t\u00e9 et la Direction informatique Groupe : mat\u00e9riel informatique, r\u00e9aliser les tickets informatiques.\nProfil :\nDe formation BAC+2 dans le domaine administratif. Vous avez une 1\u00e8re exp\u00e9rience significative sur un poste similaire.\nVous \u00eates \u00e0 l\u2019\u00e9coute, disponible, naturellement serviable afin de faciliter le quotidien de chacun, dot\u00e9(e) d\u2019un bon relationnel pour communiquer et collaborer avec l\u2019ensemble des \u00e9quipes. Vous faites preuve de capacit\u00e9 d\u2019organisation. Vous ma\u00eetrisez les outils informatiques, le Pack Office et les outils digitaux.\nConditions :\nCDI d\u00e8s que possible\nR\u00e9mun\u00e9ration : Selon exp\u00e9rience + participation + int\u00e9ressement\nType d'emploi : CDI\nAvantages :\nTitre-restaurant\nHoraires :\nTravail en journ\u00e9e", "salary": "CDI", "metier": "Standardiste et accueil H/F", "statut": "CDI", "secteur": "Standardiste et accueil H/F", "experience": "Tous niveaux d'exp\u00e9rience accept\u00e9s"}]

driver_indeed = webdriver.Firefox(executable_path=r'C:\Python310\geckodriver.exe')

poster(offresIndeed, driver_indeed)
#scrapLinkedin("Responsable de magasin", "Paris", offresIndeed = list())
"""
scrapIndeed()
scrapLinkedin()
scrapMonster()
"""
