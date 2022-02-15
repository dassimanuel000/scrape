
from tkinter import Button
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time
import json
 
my_list = list()

final_result = list()


actif = input("N'oublies pas de diminuer la taille d'ecran :\n")

driver = webdriver.Firefox()
#WebDriverWait wait =  WebDriverWait(driver, 10);
#target_size = driver.Dimension.new(1600, 1268)
#driver.manage.window.size = target_size
driver.get("https://www.google.com/")
time.sleep(3)
driver.get("https://www.monster.com/job-openings/agent-de-s%C3%A9curit%C3%A9-confirm%C3%A9-ads-h-f-paris-11--6b8fb199-240f-4f4e-beb2-a8074c843726?sid=53ba83b7-4403-470c-bfcc-bc98df918e2b&jvo=m.go.sg.45&_ga=2.170450083.287345578.1644405074-1859323056.1644405074/")
time.sleep(1)
#driver.get("https://www.monster.com/jobs/search?q=gra&where=paris&page=1")

time.sleep(4)
print('ok on attend 5sec')


date = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div[2]/div[1]/div/div[1]/div/div[4]/div[2]").text
print(date)

url = driver.current_url
print(url)


titre = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div[1]/div[2]/div[1]/div[2]/h1]").text
print(titre)

contrat = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div[2]/div[1]/div/div[1]/div/div[2]/div[2]/span").text
print(contrat)


description = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div[2]/div[1]/div/div[2]/div").text
#print(description)

salary = "A négocier"

metier = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div[1]/div[2]/div[1]/div[2]/h1").text
print(metier)

statut = "Cadre du secteur privé"

secteur = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[2]/a/div/div[2]").text
print(secteur)

experience = "Tous niveaux d'expérience acceptés"


myDict = {}
myDict["date"] = date
myDict["url"] = url
myDict["titre"] = titre
myDict["contrat"] = contrat
myDict["description"] = description
myDict["salary"] = salary
myDict["metier"] = metier
myDict["statut"] = statut
myDict["secteur"] = secteur
myDict["experience"] = experience

#print(myDict)

final_result.append(myDict)

def scroll_function(i):
    #scroll=driver.find_element_by_xpath("/html/body/section[8]")
    #scroll.location_once_scrolled_into_view
    #new_height = scroll.location_once_scrolled_into_view['y']
    #print(scroll.location_once_scrolled_into_view['y'])
    height = i * 1000
    time.sleep(1.3)
    driver.execute_script("window.scrollTo("+ str(height) +", "+ str(height) +")")
    time.sleep(1.3)

#for i in range(5):
#    scroll_function(i)

#buttons = driver.find_elements_by_xpath("//a[contains(text(), 'Read More')]")

#for btn in buttons:
#    btn.click()

#driver.execute_script("window.scrollTo(0, 4000)") CA DONNE
#scroll=driver.find_element_by_xpath("/html/body/div[1]/footer")

#scroll.location_once_scrolled_into_view
#hidden_element = driver.find_elements_by_xpath('/html/body/div[1]/div[3]/main/div[2]/nav/section[1]/div[2]/div/div/div/div[46]/button') #this one is not
#for i in hidden_element:
#    if i.is_displayed():
#        print ("Element found")
#    else:
#        print ("Element not found")


