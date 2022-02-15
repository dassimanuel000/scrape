
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
    return TAG_RE.sub('', description)

#actif = input("Nous pas de diminuer la taille d'ecran :\n")

driver = webdriver.Firefox()
driver.get("https://google.com/")

print('ok on attend 5sec')

cookieGoogle = driver.find_element_by_id('L2AGLb').click()
if cookieGoogle:
    print("GOOGLE a changé l'id recupere le nouveau")
else:
    print("Init Google...")
    #On valide les cookies
    driver.get("https://www.monster.com/")
    time.sleep(3)
    #On attend la page charge
    print("On attend le site charge...")
    vocation = input("Entrer le type de métiers à récupérer:\n")
    location = input("Entrer La localité ** france si pas précise **:\n")
    print(f'On cherche les jobs de "{vocation}" près de "{location}"')

    inputElement = driver.find_elements_by_xpath('//input[contains(@placeholder, "Job Title or Keyword")]')
    time.sleep(1)
    for i in inputElement:
        nom = i.send_keys(vocation)
        print("metier ADD")
    time.sleep(1)
    parentElement = driver.find_element_by_xpath("/html/body/div[1]/div[1]/main/section[1]/div/div/div/div[1]/div/div/div/div/div[1]/div[2]/form/div/div[2]/div/div/div[2]")
    #locationElement = driver.find_elements_by_xpath('//input[contains(@placeholder, "Location")]')
    locationElement = parentElement.find_elements_by_tag_name("input")
    time.sleep(1)
    for j in locationElement:
        n_ = j.send_keys(location)
        print("location ADD")

    Search = driver.find_element_by_xpath("/html/body/div[1]/div[1]/main/section[1]/div/div/div/div[1]/div/div/div/div/div[1]/div[2]/form/div/div[2]/button").click()
    input("PAGE DES RESULTATS OUVERTS CLIQUEZ QUELQUES PART | ELARGIT L'ÉCRAN \n")
    time.sleep(2)

    #firstReslut = driver.find_element_by_xpath("/html/body/div[1]/div[3]/main/div[2]/nav/section[1]/div[2]/div[1]/div/div/div/div/div[1]/article").click()
    
    #SI IL Y A PLUSIEURS RESULTATS N'HESITE PAS A AUGMENTER LE range
    for i in range(12):
        scroll=driver.find_element_by_id("card-scroll-container")
        scroll.send_keys(Keys.PAGE_DOWN)
        time.sleep(1.3)
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #scroll_function(i)
    try:
        buttons = driver.find_element_by_xpath("//button[contains(text(), 'Load more')]").click()
    except NoSuchElementException:  #spelling error making this code not work as expected
        pass

    links = driver.find_elements_by_xpath('//article[contains(@class, "job-cardstyle__JobCardComponent-sc-1mbmxes-0")]//a[contains(@href, "job-openings")]')
    #for btn in buttons:
    #    btn.click()
    count = (len(links))
    print(count)
    
    input("VOUS POUVEZ ALLEZ SUR LA PAGE ESSYAEZ DE CHARGEZ PLUS \n")
    links = driver.find_elements_by_xpath('//article[contains(@class, "job-cardstyle__JobCardComponent-sc-1mbmxes-0")]//a[contains(@href, "job-openings")]')
    count = (len(links))
    print(count)

    for i in range(1, count):
        time.sleep(2)
        print('ok on attend 2sec---------------------------------------------------------------------------------------')
        countReslut = driver.find_element_by_xpath("/html/body/div[1]/div[3]/main/div[2]/nav/section[1]/div[2]/div[1]/div/div/div/div/div["+ str(i) +"]/article").click()

        try:
            date = driver.find_element_by_xpath("/html/body/div[1]/div[3]/main/div[2]/nav/section[1]/div[2]/div[1]/div/div/div/div/div["+ str(i) +"]/article/footer/div/span").text
        except NoSuchElementException:  #spelling error making this code not work as expected
            date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
            pass
        print(date)

        url = driver.find_elements_by_xpath("/html/body/div[1]/div[3]/main/div[2]/nav/section[1]/div[2]/div[1]/div/div/div/div/div["+ str(i) +"]/article/div/a")
        for i in url:
            url = (i.get_attribute('href'))
        print(url)

        try:
            titres = driver.find_elements_by_xpath('//div[contains(@class, "headerstyle__")]//h1[contains(@class, "JobViewTitle")]')
            for i_titre in titres:
                titre = (i_titre.get_attribute('innerHTML'))
        except NoSuchElementException:  #spelling error making this code not work as expected
            titre = vocation
            pass
        print(titre)


        try:
            villes = driver.find_elements_by_xpath('//div[contains(@class, "headerstyle__")]//h3[contains(@class, "headerstyle__JobViewHeaderLocation")]')
            for i_ville in villes:
                ville = (i_ville.get_attribute('innerHTML'))
        except NoSuchElementException:  #spelling error making this code not work as expected
            ville = location
            pass
        print(ville)


        time.sleep(1)

        try:
            descriptions = driver.find_elements_by_xpath('//div[contains(@class, "descriptionstyles__")]//div[contains(@class, "descriptionstyles__DescriptionBody")]')
            for i_description in descriptions:
                description = (i_description.get_attribute('innerHTML'))
                description = remove_tags(description)
        except NoSuchElementException:  #spelling error making this code not work as expected
            description = "Contactez l'employeur"
            pass
        print(description)

        
        try:
            salary = "A Définir"
            salarys = driver.find_elements_by_xpath('//div[contains(@class, "detailsstyles__")]//div[contains(@data-test-id, "svx-jobview-salary-or-companysize")]')
            for i_salary in salarys:
                salary = (i_salary.get_attribute('innerHTML'))
        except NoSuchElementException:  #spelling error making this code not work as expected
            salary = "A Définir"
            pass
        print(salary)

        try:
            contrats = driver.find_elements_by_xpath('//div[contains(@class, "detailsstyles__")]//div[contains(@data-test-id, "svx-jobview-employmenttype")]')
            for i_contrat in contrats:
                contrat = (i_contrat.get_attribute('innerHTML'))
        except NoSuchElementException:  #spelling error making this code not work as expected
            contrat = "CDI"
            pass
        print(contrat)
        
        metier = vocation

        statut = "Cadre du secteur privé"

        secteur = vocation

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

        #print(myDict)

        final_result.append(myDict)


with open("res.json", "wb") as writeJSON:
   jsStr = json.dumps(final_result)
   # the decode() needed because we need to convert it to binary
   writeJSON.write(jsStr.encode('utf-8')) 
print ('end')
    

    

    

