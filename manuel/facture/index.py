
from selenium import webdriver
import re
 
my_list = list()

final_result = list()

    
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(description):
    return TAG_RE.sub(' ', description)

#actif = input("Nous pas de diminuer la taille d'ecran :\n")

#driver = webdriver.Firefox()

driver = webdriver.Chrome(executable_path=r'C:\Python310\chromedriver.exe')
driver.get("https://dev.life-cm.com/facture_fourniture")

print('ok on attend 5sec')

input("VERIF \n")
links = driver.find_elements_by_xpath('//a[contains(@href, "fourn_BILAN")]')
count = (len(links))

#for i in range(0, count):
#    countReslut = driver.find_element_by_xpath('//*[@id="fourn_BILAN'+ str(i) +'"]').click()

    
    
links = driver.find_elements_by_xpath('//a[contains(@href, "fourn_RAPPORT")]')
count = (len(links))
print(count)
for i in range(0, count):
    countReslut = driver.find_element_by_xpath('//*[@id="fourn_RAPPORT'+ str(i) +'"]').click()

input("VERIF \n")