
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
    urlParent = urlParent + "&fromage=3&limit=50&sort=date&filter=0"
    driver.get(urlParent)
    time.sleep(3)
    #On attend la page charge
    print("On attend le site charge ...")


    onetrust = driver.find_element_by_xpath('//*[@id="onetrust-reject-all-handler"]').click()
    time.sleep(1)
    print("VALIDE COOKIE")

    links = driver.find_elements_by_xpath('/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[5]/div/a')
    count = (len(links))
    if count < 3: 
        recapcha()
        time.sleep(2)
        recapcha()
        time.sleep(1)
        links = driver.find_elements_by_xpath('/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[5]/div/a')
        count = (len(links))
        print(count)
    else:
        print(count)
    
    input("PAGE DES RESULTATS OUVERTS CLIQUEZ QUELQUES PART | ELARGIT L'ÉCRAN \n")

    for i in links:
        step1 = (i.get_attribute('href'))
        my_list.append(step1)
        
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
        titre = driver.find_elements_by_xpath('//div[contains(@class, "jobsearch-JobInfoHeader-title-container")]//h1[contains(@class, "jobsearch-JobInfoHeader-title")]')
        for i in titre: 
            titre = (i.get_attribute('innerHTML'))
        print(titre)

        try:
            villes = driver.find_elements_by_xpath('//div[contains(@class, "jobsearch-DesktopStickyContainer-subtitle")]//div//div')
            #villes = driver.find_elements_by_xpath('/html/body/div[1]/div[1]/div/div[3]/div/div/div[1]/div[1]/div[3]/div[1]/div[2]/div/div/div/div[2]')
            for i_ville in villes:  
                ville = i_ville.get_attribute('innerHTML')
                ville = remove_tags(ville)
                ville = ville + " , France"
        except NoSuchElementException:  #spelling error making this code not work as expected
            ville = "France"
            pass
        print(ville)


        time.sleep(1)

        try:
            descriptions = driver.find_elements_by_xpath('//div[contains(@id, "jobDescriptionText")]')
            for i_description in descriptions:
                description = (i_description.get_attribute('innerHTML'))
                description = remove_tags(description)
        except NoSuchElementException:  #spelling error making this code not work as expected
            description = "Contactez l'employeur"
            pass
        print(description)

        
        try:
            salary = "A Définir"
            salarys = driver.find_elements_by_xpath('//div[contains(@id, "salaryInfoAndJobType")]//span[contains(@class, "attribute_snippet")]')
            for i_salary in salarys:
                salary = (i_salary.get_attribute('innerHTML'))
                salary = ''.join([n for n in salary if n.isdigit()])
                diff = len(salary)
                diff = (diff / 2)
                
                salary = salary[int(0):int(diff)]
        except NoSuchElementException:  #spelling error making this code not work as expected
            salary = "A Définir"
            pass
        print(salary)

        try:
            contrat = "CDI"
            contrats = driver.find_elements_by_xpath('//div[contains(@id, "salaryInfoAndJobType")]//span[contains(@class, "jobsearch-JobMetadataHeader-item")]')
            for i_contrat in contrats:
                contrat = (i_contrat.get_attribute('innerHTML'))
                contrat = remove_tags(contrat)
        except NoSuchElementException:  #spelling error making this code not work as expected
            contrat = "CDI"
            pass
        print(contrat)
        
        metier = titre

        statut = contrat

        secteur = titre.split()[0]

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

        final_result.append(myDict)


with open("res.json", "wb") as writeJSON:
   jsStr = json.dumps(final_result)
   # the decode() needed because we need to convert it to binary
   writeJSON.write(jsStr.encode('utf-8')) 
print ('end')
    

    

