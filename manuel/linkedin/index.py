
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime

import re
import time
import json
 
my_list = list()

final_result = list()


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
        driver.find_element_by_xpath("//a[contains(@onclick,'closeGoogleOnlyModal')]").click()
        recapcha = driver.find_element_by_id("popover-background").click()
    except NoSuchElementException:  #spelling error making this code not work as expected
        pass

#actif = input("Nous pas de diminuer la taille d'ecran :\n")

#driver = webdriver.Firefox()
driver = webdriver.Firefox(executable_path=r'C:\Python310\geckodriver.exe')
driver.get("https://google.com/")

print('ok on attend 5sec')

cookieGoogle = driver.find_element_by_id('L2AGLb').click()
if cookieGoogle:
    print("GOOGLE a changé l'id recupere le nouveau")
else:
    print("Init Google...")
    #On valide les cookies
    urlParent = input("Entrer le lien de la page juste avec les mots clés et la location:\n")
    driver.get(urlParent)
    time.sleep(3)
    #On attend la page charge
    print("On attend le site charge ...")


    onetrust = driver.find_element_by_xpath('//button[contains(@action-type, "ACCEPT")]').click()
    time.sleep(1)
    print("VALIDE COOKIE")

    for i in range(4):
        scroll=driver.find_elements_by_xpath("/html/body/div[1]/footer")[0]
        scroll.location_once_scrolled_into_view
        time.sleep(1.3)
    

    links = driver.find_elements_by_xpath('/html/body/div[1]/div/main/section[2]/ul/li/div/a')
    count = (len(links))                    
    if count < 4:
        driver.refresh()
        time.sleep(1)
        links = driver.find_elements_by_xpath('/html/body/div[1]/div/main/section[2]/ul/li/div/a')
        count = (len(links))
        print(count)
    else:
        print(count)
    for i in links:
        step1 = (i.get_attribute('href'))
        my_list.append(step1)
    #-------------------------------------------------------------------------------------------------------------
    links_2 = driver.find_elements_by_xpath('/html/body/div[1]/div/main/section[2]/ul/li/a')
    count_2 = (len(links_2))                    
    if count_2 < 4:
        time.sleep(1)
        links_2 = driver.find_elements_by_xpath('/html/body/div[1]/div/main/section[2]/ul/li/a')
        count_2 = (len(links_2))
        print(count_2)
    else:
        print(count_2)

    for i_2 in links_2:
        step2 = (i_2.get_attribute('href'))
        my_list.append(step2)
        
    print("on a tout les liens des offres")
    print(my_list)

    input("PAGE DES RESULTATS OUVERTS CLIQUEZ QUELQUES PART | ELARGIT L'ÉCRAN \n")

    #for increment in range(1, count):
    for j in my_list:
        driver.get(j)
        time.sleep(2)
        recapcha()
        print('ok on a ttend 2sec---------------------------------------------------------------------------------------')
        
        #countReslut = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[5]/div/a["+ str(increment) +"]").click()

        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        print(date)

        url = j
        print(url)
        titre = driver.find_elements_by_xpath('//div[contains(@class, "top-card-layout__entity-info")]//h1[contains(@class, "topcard__title")]')
        for i in titre: 
            titre = (i.get_attribute('innerHTML'))
        print(titre)

        try:
            villes = driver.find_elements_by_xpath('//div[contains(@class, "topcard__flavor-row")]//span[contains(@class, "topcard__flavor--bullet")]')
            for i_ville in villes:
                ville = i_ville.text
                ville = ville + ", France"
        except NoSuchElementException:  #spelling error making this code not work as expected
            ville = "France"
        print(ville)


        time.sleep(1)

        try:
            descriptions = driver.find_elements_by_xpath('//section[contains(@class, "show-more-less-html")]//div[contains(@class, "show-more-less-html__markup")]')
            for i_description in descriptions:
                description = (i_description.get_attribute('innerHTML'))
                description = remove_tags(description)
        except NoSuchElementException:  #spelling error making this code not work as expected
            description = "Contactez l'employeur"
            pass
        print(description)

        
        salary = "A Définir"
        print(salary)

        try:
            contrat = "CDI"
            contrats = driver.find_elements_by_xpath('/html/body/main/section[1]/div/div[1]/section[1]/div/ul/li[2]/span')
            for i_contrat in contrats:
                contrat = (i_contrat.get_attribute('innerHTML'))
                contrat = remove_tags(contrat)
        except NoSuchElementException:  #spelling error making this code not work as expected
            contrat = "CDI"
            pass
        print(contrat)
        
        
        try:
            metier = titre
            metiers = driver.find_elements_by_xpath('/html/body/main/section[1]/div/div[1]/section[1]/div/ul/li[3]/span')
            for i_metier in metiers:
                metier = (i_metier.get_attribute('innerHTML'))
        except NoSuchElementException:  #spelling error making this code not work as expected
            metier = titre
            pass
        print(metier)

        try:
            statut = " A DEFINIR"
            statuts = driver.find_elements_by_xpath('/html/body/main/section[1]/div/div[1]/section[1]/div/ul/li[1]/span')
            for i_statut in statuts:
                statut = (i_statut.get_attribute('innerHTML'))
        except NoSuchElementException:  #spelling error making this code not work as expected
            statut = " A DEFINIR"
            pass
        print(statut)

        try:
            secteur = titre
            secteurs = driver.find_elements_by_xpath('/html/body/main/section[1]/div/div[1]/section[1]/div/ul/li[4]/span')
            for i_secteur in secteurs:
                secteur = (i_secteur.get_attribute('innerHTML'))
        except NoSuchElementException:  #spelling error making this code not work as expected
            secteur = titre
            pass
        print(secteur)

        experience = statut


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

        final_result.append(myDict)


with open("res.json", "wb") as writeJSON:
   jsStr = json.dumps(final_result)
   # the decode() needed because we need to convert it to binary
   writeJSON.write(jsStr.encode('utf-8')) 
print ('end')
    

    

