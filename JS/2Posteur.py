import importlib.util

importlib.util.module_for_loader
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
options = Options()
options.add_argument("--disable-notifications")
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
	client = MongoClient("mongodb://192.168.1.174:27017/")
	print("Connected successfully!!!")
except:
	print("Could not connect to MongoDB")

db = client.VRio
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
    'categorie':[]
}


for i in range(taille):
    cleanerDict["id"].append(i)
    cleanerDict["date"].append(x[i]["date"])
    cleanerDict["url"].append(x[i]["url"])
    cleanerDict["titre"].append(x[i]["titre"])
    cleanerDict["ville"].append(x[i]["ville"])
    cleanerDict["contrat"].append(x[i]["contrat"])
    cleanerDict["description"].append(x[i]["description"])
    cleanerDict["salary"].append(x[i]["salary"])
    cleanerDict["metier"].append(x[i]["metier"])
    cleanerDict["statut"].append(x[i]["statut"])
    cleanerDict["secteur"].append(x[i]["secteur"])
    cleanerDict["experience"].append(x[i]["experience"])
    cleanerDict["lieux"].append(x[i]["lieux"])
    cleanerDict["categorie"].append(x[i]["categorie"])
    
# en guise de test
# for z in cleanerDict["titre"]:
#     print(z)
i = 0

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.cache.disk.enable", False)
profile.set_preference("browser.cache.memory.enable", False)
profile.set_preference("browser.cache.offline.enable", False)
profile.set_preference("network.http.use-cache", False) 
driver = webdriver.Firefox(options=options, firefox_profile=profile)
driver.get("https://trouver-un-candidat.com/wp-admin")
driver.maximize_window()
idLogin = 'user_login'
login = 'annoncetrouveruncandidat'
tryAndRetryFillById(driver, idLogin, login)
del idLogin, login

idMdp = 'user_pass'
mdp = '(%)Sku&mv#35OewiC%'
tryAndRetryFillById(driver, idMdp, mdp)
del idMdp, mdp

idSubmit = 'wp-submit'
waitBeforeClickOnId(driver, idSubmit)
del idSubmit

# len(cleanerDict["id"]

while i < len(cleanerDict["id"]):
    print(Fore.GREEN + str(i + 1)+ 'e boucle dans la bdd' + Style.RESET_ALL)
    listLieux = cleanerDict["lieux"][i].split('/')
    driver.get('https://trouver-un-candidat.com/wp-admin/post-new.php?post_type=job_listing')

    time.sleep(5)

    # retrait de la pop up
    if i == 0:
        try:
            xPathPopUp = '//div[contains(@class,"components-modal__header")]//button[@aria-label="Fermez la boite de dialogue"]'
            tryAndRetryClickXpath(driver, xPathPopUp)
        except:
            time.sleep(5)
            xPathPopUp = '//div[contains(@class,"components-modal__header")]//button[@aria-label="Fermez la boite de dialogue"]'
            tryAndRetryClickXpath(driver, xPathPopUp)

    # récupération élément et affichage du titre
    now = datetime.now()
    current_time = now.strftime("%H %M%S")
    xPathTitle = '//h1[@aria-label="Intitulé du poste"]'
    titre = str(cleanerDict["titre"][i])  + ' ' + str(listLieux[1]) +  ' - ' + str(current_time) + '*°'
    tryAndRetryFillByXpath(driver, xPathTitle, titre)

    # clique sur l'onglet emploi
    try:
        xpathEmploi = '/html/body/div[1]/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div/div[2]/ul/li[1]/button'
        tryAndRetryClickXpath(driver, xpathEmploi)
    except NoSuchElementException:
        pass

    # fonctionnalités catégories
    xpathCategorie = '/html/body/div[1]/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div/div[3]/div[4]/h2/button'
    if i == 0:
        tryAndRetryClickXpath(driver, xpathCategorie)
    listCat = cleanerDict["categorie"][i].split('/')
    o = 0
    xPathSearchCategorie = f'//input[@id="inspector-text-control-{str(o)}"]'
    tryAndRetryClickXpath(driver, xPathSearchCategorie)
    z = 0
    while z < len(listCat):
        idCheckbox = f'//label[contains(., "{listCat[z]}")]'
        tryAndRetryFillByXpath(driver, xPathSearchCategorie, listCat[z])
        try:
            t = driver.find_element(By.XPATH, idCheckbox).click()
        except:
            pass
        driver.find_element(By.XPATH,xPathSearchCategorie).clear()
        z = z + 1

    # fonctionnalités lieux
    xPathLieux = '/html/body/div[1]/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div/div[3]/div[5]/h2/button'
    if i == 0:
        tryAndRetryClickXpath(driver, xPathLieux)
    xPathSearchLieux = f'//input[@id="inspector-text-control-{str(o +1)}"]'
    tryAndRetryClickXpath(driver, xPathSearchLieux)
    z = 0
    while z < len(listLieux):
        idCheckbox = f'//label[contains(., "{listLieux[z]}")]'
        tryAndRetryFillByXpath(driver, xPathSearchLieux, listLieux[z])
        try:
            t = driver.find_element(By.XPATH, idCheckbox).click()
        except:
            pass
        driver.find_element(By.XPATH,xPathSearchLieux).clear()
        z = z + 1

    # envoie du texte dans la description du post
    xPathPlusTexte = '/html/body/div[1]/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div[3]/div[2]/div/div[2]/div[2]/div/div/div/button'
    tryAndRetryClickXpath(driver, xPathPlusTexte)
    xPathParagraphe = "//button[contains(@class,'components-button block-editor-block-types-list__item editor-block-list-item-paragraph')]"
    tryAndRetryClickXpath(driver, xPathParagraphe)
    xPathDescription = "//p[contains(@class,'block-editor-rich-text__editable block-editor-block-list__block wp-block is-selected wp-block-paragraph rich-text')]"
    descriptionRobot = str(cleanerDict['description'][i])
    driver.find_element(By.XPATH, xPathDescription).send_keys(descriptionRobot)
    time.sleep(5)

    # envoie du texte pour un lien externe
    xPathElementToScroll = '/html/body/div[1]/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[2]'
    tryAndRetryClickXpath(driver, xPathElementToScroll)
    n = 11
    actions = ActionChains(driver) 
    actions.send_keys(Keys.TAB * n)
    actions.perform()
    print(Fore.RED + 'press tab complete' + Style.RESET_ALL)
    # time.sleep(10)
    
    actions.send_keys(Keys.ENTER)
    actions.perform()
    print(Fore.YELLOW + 'press enter complete' + Style.RESET_ALL)
    # time.sleep(10)
    
    actions.send_keys(Keys.ARROW_DOWN)
    actions.perform()
    print(Fore.BLUE + 'press down complete' + Style.RESET_ALL)
    # time.sleep(10)
    
    actions.send_keys(Keys.ENTER)
    actions.perform()
    print(Fore.YELLOW + 'press enter complete' + Style.RESET_ALL)
    # time.sleep(10)

    xPathUrlExt = '//*[@id="_job_apply_url"]'
    driver.find_element(By.XPATH, xPathUrlExt).send_keys(cleanerDict["url"][i])

    # Validation du poste
    time.sleep(10)
    xPathValidationPoste = '/html/body/div[1]/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/div[3]/button[2]'
    tryAndRetryClickXpath(driver, xPathValidationPoste)
    
    # commenté cette ligne si y'a bug
    # time.sleep(15)
    # waitBeforeClickOnXpath(driver, xPathValidationPoste)
    try:
        waitBeforeClickOnXpath(driver, xPathValidationPoste)
    except:
        pass
    
    xPathConfirmation = '/html/body/div[1]/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[4]/div[2]/div/div/div[1]/div[1]/button'
    tryAndRetryClickXpath(driver, xPathConfirmation)
    i = i + 1

driver.delete_all_cookies()
driver.quit()
del db, cleanerDict, col, x, driver, taille, options
