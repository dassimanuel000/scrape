
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
driver.get("https://ceo.life-cm.com/")

print('ok on attend 5sec')

#driver.execute_script("window.scrollTo(0, 4000)") CA DONNE
scroll=driver.find_element_by_xpath("/html/body/section[7]/div")

scroll.location_once_scrolled_into_view
