# coding=utf-8
from selenium import webdriver
import time
import json

res = list()
output = {"nom":"Wuster","titre":"Recherche Électricien", "tel": "135"}
out = {"nom":"DASS","titre":"NFOEDX Électricien"}


#res += output
#res += out

res.append(out)

print(res)


 
 
driver = webdriver.Firefox()
driver.get("https://www.crit-job.com/offres/voir/630326-chef-de-rayon-maree-hf")

time.sleep(3)
#On attend la page charge
print('ok on attend 5sec')

driver.find_element_by_id('tarteaucitronPersonalize2').click()
#On valide les cookies

links = driver.find_elements_by_xpath('//div[contains(@class, "box_inf_left")]//h3[contains(@title, "")]')
for i in links:
    nom = i.get_attribute('title')
    print(nom)

titre = driver.find_elements_by_class_name("title_offer_box")
for i in titre:
    titre = i.text
    print(titre)


description = driver.find_element_by_xpath("/html/body/div[4]/div/section/div[2]/section[2]").text
print(description)


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

myDict = {}
myDict["nom"] = nom
myDict["titre"] = titre
myDict["description"] = description
myDict["addresse"] = addresse
myDict["travail"] = travail
myDict["date"] = date
myDict["telephone"] = telephone

print(myDict)

res.append(myDict)

#with open('res.json', 'w') as f:
#   json.dump(res, f, ensure_ascii=False, indent=4)

with open("res.json", "wb") as writeJSON:
   jsStr = json.dumps(res)
   # the decode() needed because we need to convert it to binary
   writeJSON.write(jsStr.decode('utf-8')) 
print ('end')



    