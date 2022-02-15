
from selenium import webdriver
import time
import json
 
my_list = list()

final_result = list()


driver = webdriver.Firefox()
driver.get("https://www.crit-job.com/offres?page_limit=60&token=4f5f9c927a20179c1c361adfb8dce24c")

time.sleep(3)
#On attend la page charge
print('ok on attend 5sec')

driver.find_element_by_id('tarteaucitronPersonalize2').click()
#On valide les cookies

links = driver.find_elements_by_xpath('//h2[contains(@class, "title_offer_box")]//a[contains(@href, "offres")]')
for i in links:
    step1 = (i.get_attribute('href'))
    my_list.append(step1)
    
print("on a tout les liens des offres")
print(my_list)

for j in my_list:
    driver.get(j)
    time.sleep(3)
    print("one by one")
    links = driver.find_elements_by_xpath('//div[contains(@class, "box_inf_left")]//h3[contains(@title, "")]')
    for i in links:
        nom = i.get_attribute('title')
        print(nom)

    titre = driver.find_elements_by_class_name("title_offer_box")
    for i in titre:
        titre = i.text
        print(titre)


    description = driver.find_element_by_xpath("/html/body/div[4]/div/section/div[2]/section[2]").text
    #print(description)


    addresse = driver.find_element_by_xpath("/html/body/div[4]/div/section/div[2]/section[1]/ul[1]/li[3]").text
    addresse = addresse.replace("Lieu de travail :", "") 
    print(addresse)

    travail = driver.find_element_by_xpath("/html/body/div[4]/div/section/div[2]/section[1]/ul[1]/li[2]").text
    travail = travail.replace("Metier :", "")
    print(travail)

    date = driver.find_element_by_xpath("/html/body/div[4]/div/section/div[2]/header/label").text
    date = date.replace("/ 22", "/ 2022")
    print(date)

    telephone = driver.find_element_by_xpath("/html/body/div[4]/div/section/div[1]/div[1]/div/section/p[3]").text
    print(telephone)

    contrat = "CDI"
    salary = "A Définir"
    statut = "Cadre du secteur privé"
    experience = "Tous niveaux d'expérience acceptés"


    myDict = {}
    myDict["date"] = date
    myDict["url"] = j
    myDict["titre"] = titre
    myDict["ville"] = addresse
    myDict["contrat"] = contrat
    myDict["description"] = description
    myDict["salary"] = salary
    myDict["metier"] = travail
    myDict["statut"] = telephone
    myDict["secteur"] = nom
    myDict["experience"] = experience

    #print(myDict)

    final_result.append(myDict)
    


with open("res.json", "wb") as writeJSON:
   jsStr = json.dumps(final_result)
   # the decode() needed because we need to convert it to binary
   writeJSON.write(jsStr.encode('utf-8')) 
print ('end')
