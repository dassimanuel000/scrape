
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time
import json
 
my_list = list()

final_result = list()


actif = input("Nous pas de diminuer la taille d'ecran :\n")

driver = webdriver.Firefox()
#WebDriverWait wait =  WebDriverWait(driver, 10);
#target_size = driver.Dimension.new(1600, 1268)
#driver.manage.window.size = target_size
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
    input("PAGE DES RESULTATS OUVERTS | DIMINUE L'ÉCRAN \n")
    time.sleep(2)
    

