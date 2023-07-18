import importlib.util
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import InvalidSelectorException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import InvalidSelectorException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert 
from selenium.webdriver.chrome.service import Service
from datetime import datetime
importlib.util.module_for_loader
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
options = Options()
options.add_argument("--disable-notifications")
options.add_argument('--headless')
options.add_argument('--disable-gpu') 
try:
    from headers.headerSelenium import *
except ModuleNotFoundError:
    importlib.util.module_for_loader
    
try:
    from headers.headerSeleniumPoster import *
except ModuleNotFoundError:
    importlib.util.module_for_loader
    
try:
    from headers.headerPyMonGo import *
except ModuleNotFoundError:
    importlib.util.module_for_loader
    
try:
	client = MongoClient("mongodb://localhost:27017/")
	print("Connected successfully!!!")
except:
	print("Could not connect to MongoDB")

db = client.VSuperOrdiTalent
col = db['regionjob_annonce']
x = col.find()
x = list(x)
taille = len(x)
# pprint(x)
# pprint(taille)

cleanerDict = {
    'id' : [],
    'date' : [],
    'url' : [],
    'titre' : [],
    'ville' : [],
    'contrat' : [],
    'description' : [],
    'salary' : [],
    'metier' : [],
    'statut' : [],
    'secteur' : [],
    'experience' : [],
    'lieux': [],
    'categorie':[],
    'compagny': [],
    'skills' : []
}


for i in range(taille):
    cleanerDict["id"].append(i)
    cleanerDict["date"].append(x[i]["date"])
    cleanerDict["url"].append(x[i]["url"])
    cleanerDict["titre"].append(x[i]["titre"])
    try:
        cleanerDict["ville"].append(x[i]["ville"])
    except:
        cleanerDict["ville"].append("pas de ville")
    try:
        cleanerDict["contrat"].append(x[i]["contrat"])
    except:
        cleanerDict["contrat"].append("CDI")
    cleanerDict["description"].append(x[i]["description"])
    try:
        cleanerDict["salary"].append(x[i]["salary"])
    except:
        cleanerDict["salary"].append("pas de salaire")
    try:
        cleanerDict["metier"].append(x[i]["metier"])
    except:
        cleanerDict["metier"].append("pas de metier")

    try:
        cleanerDict["statut"].append(x[i]["statut"])
    except:
        cleanerDict["statut"].append("pas de statut")
    try:
        cleanerDict["secteur"].append(x[i]["secteur"])
    except:
        cleanerDict["secteur"].append("pas de secteur")
    try:
        cleanerDict["experience"].append(x[i]["experience"])
    except:
        cleanerDict["experience"].append("pas de experience")
    cleanerDict["lieux"].append(x[i]["lieux"])
    cleanerDict["categorie"].append(x[i]["categorie"])
    try:
        cleanerDict["compagny"].append(x[i]["compagny"])
    except:
        cleanerDict["compagny"].append("Entreprise non renseigne")
    try:
        cleanerDict["skills"].append(x[i]["skills"])
    except:
        cleanerDict["skills"].append("Competences non renseignees")
    
# en guise de test
# for z in cleanerDict["titre"]:
#     print(z)
i = 0


profile = webdriver.FirefoxProfile()
profile.set_preference("browser.cache.disk.enable", False)
profile.set_preference("browser.cache.memory.enable", False)
profile.set_preference("browser.cache.offline.enable", False)
profile.set_preference("network.http.use-cache", False) 
driver = webdriver.Firefox(executable_path='/home/jeremy/Documents/ScriptsRio/ScriptsRio/ScriptPosteurIndeed/geckodriver', options=options, firefox_profile=profile)
driver.get("https://emploi-talent.com/wp-admin")
driver.maximize_window()
idLogin = 'user_login'
login = 'AdminSen'
tryAndRetryFillById(driver, idLogin, login)
del idLogin, login

idMdp = 'user_pass'
mdp = 'ZjR()BlCKKHMnRIr(8'
tryAndRetryFillById(driver, idMdp, mdp)
del idMdp, mdp

idSubmit = 'wp-submit'
waitBeforeClickOnId(driver, idSubmit)
del idSubmit

# len(cleanerDict["id"]

while i < len(cleanerDict["id"]):
    print(Fore.GREEN + str(i + 1)+ 'e boucle dans la bdd' + Style.RESET_ALL)
    listLieux = cleanerDict["lieux"][i].split('/')
    driver.get('https://emploi-talent.com/wp-admin/post-new.php?post_type=job_listing')

    time.sleep(5)

    # retrait de la pop up
    if i == 0:
        xPathPopUp = '//div[contains(@class,"components-modal__header")]//button[@aria-label="Fermez la boite de dialogue"]'
        try:
            tryAndRetryClickXpathXTimes(driver, xPathPopUp, 3)
        except NoSuchElementException:
            pass

    # récupération élément et affichage du titre
    now = datetime.now()
    current_time = now.strftime("%H %M%S")
    xPathTitle = '//h1[@aria-label="Intitulé du poste"]'
    titre = str(cleanerDict["titre"][i])  + ' ' + str(listLieux[1]) +  ' - ' + str(current_time)
    tryAndRetryFillByXpath(driver, xPathTitle, titre)

    # clique sur l'onglet emploi
    try:
        xpathEmploi = '//*[@id="editor"]/div/div[1]/div[1]/div[2]/div[3]/div/div[2]/ul/li[1]/button'
        element2 = driver.find_element(By.XPATH, xpathEmploi)
        element2.click()
        #tryAndRetryClickXpath(driver, xpathEmploi)
    except NoSuchElementException:
        print ('job non visible')
        xpathAutreElement = '//*[@id="editor"]/div/div[1]/div[1]/div[1]/div/div[3]/div[2]/button[1]'
        element = driver.find_element(By.XPATH, xpathAutreElement)
        element.click()
        element2 = driver.find_element(By.XPATH, xpathEmploi)
        element2.click()
        print ('on essaie de cliquer sur job a nouveau')

    # fonctionnalités catégories
    xpathCategorie = '//*[@id="editor"]/div/div[1]/div[1]/div[2]/div[3]/div/div[3]/div[4]/h2/button'

    xpathCategorieFormFind = '/html/body/div[1]/div[2]/div[3]/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div/div[3]/div[2]/div[2]'
    try: 
        test = driver.find_element(By.XPATH, xpathCategorieFormFind)
        print ('visible1')
    except NoSuchElementException: 
        print ('non visible1')
        driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div/div[3]/div[2]/h2/button').click()
    #if i == 0:
    #    tryAndRetryClickXpath(driver, xpathCategorie)
    listCat = cleanerDict["categorie"][i].split('/')
    o = 3
    xPathSearchCategorie = f'/html/body/div[1]/div[2]/div[3]/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div/div[3]/div[2]/div[1]/div/input'
    
    tryAndRetryClickXpath(driver, xPathSearchCategorie)
    z = 0
    print(listCat)
    while z < len(listCat):
        idCheckbox = f'//label[contains(.,"{listCat[z]}")]'
        tryAndRetryFillByXpath(driver, xPathSearchCategorie, listCat[z])
        time.sleep(2)
        try:
            t = driver.find_element(By.XPATH, idCheckbox).click()
        except:
            pass
        driver.find_element(By.XPATH,xPathSearchCategorie).clear()
        z = z + 1

    # fonctionnalités lieux
    xPathLieux = '//*[@id="editor"]/div/div[1]/div[1]/div[2]/div[3]/div/div[3]/div[5]/h2/button'

    xpathLieuxFormFind = '/html/body/div[1]/div[2]/div[3]/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div/div[3]/div[3]/div[2]'
    try: 
        test2 = driver.find_element(By.XPATH, xpathLieuxFormFind)
        print ('visible2')
    except NoSuchElementException: 
        print ('non visible2')
        driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div/div[3]/div[3]/h2/button').click()
    #if i == 0:
    #    tryAndRetryClickXpath(driver, xPathLieux)
    xPathSearchLieux = f'/html/body/div[1]/div[2]/div[3]/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div/div[3]/div[3]/div[1]/div/input'
    tryAndRetryClickXpath(driver, xPathSearchLieux)
    z = 0
    print(listLieux)
    while z < len(listLieux):
        idCheckbox = f'//label[contains(.,"{listLieux[z]}")]'
        tryAndRetryFillByXpath(driver, xPathSearchLieux, listLieux[z])
        time.sleep(2)
        try:
            t = driver.find_element(By.XPATH, idCheckbox).click()
        except:
            pass
        driver.find_element(By.XPATH,xPathSearchLieux).clear()
        z = z + 1

    # envoie du texte dans la description du post
    xPathPlusTexte = '//*[@id="editor"]/div/div[1]/div[1]/div[2]/div[2]/div[3]/div[2]/div/div[2]/div[2]/div/div/div/button'
    tryAndRetryClickXpath(driver, xPathPlusTexte)
    xPathParagraphe = "//button[contains(@class,'components-button block-editor-block-types-list__item editor-block-list-item-paragraph')]"
    tryAndRetryClickXpath(driver, xPathParagraphe)
    xPathDescription = "//p[contains(@class,'block-editor-rich-text__editable block-editor-block-list__block wp-block is-selected wp-block-paragraph rich-text')]"
    descriptionRobot = str(cleanerDict['description'][i])
    driver.find_element(By.XPATH, xPathDescription).send_keys(descriptionRobot)
    time.sleep(5)

    # envoie du texte pour un lien externe                         
    # xPathElementToScroll = '/html/body/div[1]/div[2]/div[3]/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[2]'
    # tryAndRetryClickXpath(driver, xPathElementToScroll)
    n = 9
    actions = ActionChains(driver) 
    actions.send_keys(Keys.TAB * n)
    actions.perform()
    print(Fore.RED + 'press tab complete' + Style.RESET_ALL)
    # time.sleep(10)
    
    actions.send_keys(Keys.ENTER)
    actions.perform()
    print(Fore.YELLOW + 'press enter complete' + Style.RESET_ALL)
    # time.sleep(10)
    
    
    actions.send_keys(Keys.ENTER)
    actions.perform()
    print(Fore.YELLOW + 'press enter complete' + Style.RESET_ALL)
    # time.sleep(10)

    xPathUrlExt = '//*[@id="_job_apply_url"]'
    driver.find_element(By.XPATH, xPathUrlExt).send_keys(cleanerDict["url"][i])


    xPathUrlExt = '//*[@id="textarea-id"]'
    driver.find_element(By.XPATH, xPathUrlExt).send_keys(cleanerDict["skills"][i])
    xPathUrlExt = '//*[@id="entreprise-id"]'
    driver.find_element(By.XPATH, xPathUrlExt).send_keys(cleanerDict["compagny"][i])

    # Validation du poste
    time.sleep(10)
    xPathValidationPoste = '//*[@id="editor"]/div/div[1]/div[1]/div[1]/div/div[3]/button[3]'
    tryAndRetryClickXpath(driver, xPathValidationPoste)
    
    # commenté cette ligne si y'a bug
    # time.sleep(15)
    # waitBeforeClickOnXpath(driver, xPathValidationPoste)
    try:
        waitBeforeClickOnXpath(driver, xPathValidationPoste)
    except:
        pass
    
    xPathConfirmation = '//*[@id="editor"]/div/div[1]/div[1]/div[2]/div[4]/div[2]/div/div/div[1]/div[1]/button'
    tryAndRetryClickXpath(driver, xPathConfirmation)
    i = i + 1

driver.delete_all_cookies()
driver.quit()
del db, cleanerDict, col, x, driver, taille, options
