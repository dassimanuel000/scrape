from headers.headerSelenium import *
from headers.headerExcelReader import *

colorama.init()

nombreDeBouclesListeDates = len(listeDepartement)
# len(listeDepartement)
# Début de boucle à 0 -> changer cette variable pour changer le début
compteurBouclesListeDates = 0

# listeJob = make_a_converted_list_job_null()
# listeDepartement = make_a_converted_list_departemen_null()
print(Fore.RED + str(nombreDeBouclesListeDates) + Style.RESET_ALL)
print(listeJob)
print(listeDepartement)
print(listeLieu)
print(listeCategorie)

while compteurBouclesListeDates < nombreDeBouclesListeDates:
    listeDeLiensNonClean = list()
    listeDeLiensClean = list()
    offresIndeed = list()
    
    # récupération des lieux
    lieux = listeLieu[compteurBouclesListeDates]
    # récupération des catégories
    categorie = listeCategorie[compteurBouclesListeDates]
    
    driver = webdriver.Firefox()
    driver.get("https://www.google.com")
    cookieGoogle = driver.find_element(By.ID,'L2AGLb').click()

    try:
        driver.find_element(By.CLASS_NAME, 'h-captcha')
        input(Fore.BLUE + 'Captcha à résoudre veuillez le résoudre et tapez entrez pour continuer...')
        print(Style.RESET_ALL)
    except NoSuchElementException:
        print("No captcha")
    
    if cookieGoogle:
        print("GOOGLE a changé l'id recupere le nouveau")
    else:
        print("Init Google...")
        #On valide les cookies
        urlParent = 'https://fr.indeed.com/jobs?q='+ str(make_better_job(compteurBouclesListeDates)) +'&l='+ str(make_better_dep(compteurBouclesListeDates))
        urlParent = urlParent + "&radius=25&fromage=14&limit=25&sort=date&filter=0"
        urlFinal = parse_url(urlParent)
        print(urlFinal)
        getLocation = listeLieu[compteurBouclesListeDates].split('/')
        try:
            getLocation = getLocation[1]
        except IndexError:
            getLocation = str(listeLieu[compteurBouclesListeDates])
        forJson = write_my_json(urlFinal, compteurBouclesListeDates)
        # faire fonctionner un modulo qui affichera les lettres de l'alphabet
        # if(forJson >= 10):
        #     forJson = 
        print(forJson)
        driver.get(urlParent)
        timeSleeper()
        #On attend la page charge
        print("On attend le site charge ...")

        try:
            onetrust = driver.find_element(By.XPATH,'//*[@id="onetrust-reject-all-handler"]').click()
        except NoSuchElementException:
            pass
        timeSleeper()
        print("Cookie validé")

        links = driver.find_elements(By.CLASS_NAME,'jcs-JobTitle')
        nombreDeLiens = len(links)

        # condition si y'a moins de 10 urls + 50 au radius
        if (nombreDeLiens < 5):
            urlParent = 'https://fr.indeed.com/jobs?q='+ str(make_better_job(compteurBouclesListeDates)) +'&l='+ str(make_better_dep(compteurBouclesListeDates))
            urlParent = urlParent + "&radius=50&fromage=14&limit=25&sort=date&filter=0"
            # parsing de l'url pour récupérer le titre du job et la ville du job a scrapé
            urlFinal = parse_url(urlParent)
            # print(urlFinal)
            # print(compteurBouclesListeDates)
            getLocation = listeLieu[compteurBouclesListeDates].split('/')
            getLocation = getLocation[1]
            forJson = write_my_json(urlFinal, compteurBouclesListeDates)
            timeSleeper()
            #On attend la page charge
            print("On attend le site charge ...")
            # print(forJson)
            driver.get(urlParent)
            timeSleeper()
            #On attend la page charge
            print("On attend le site charge ...")
            try:
                onetrust = driver.find_element(By.XPATH,'//*[@id="onetrust-reject-all-handler"]').click()
            except NoSuchElementException:
                pass
            timeSleeper()
            print("Cookie validé")
            links = driver.find_elements(By.CLASS_NAME,'jcs-JobTitle')
            nombreDeLiens = len(links)

        # commenté cette ligne elif si vous voulez scrapper plus de 15jobs
        if (nombreDeLiens > 17):
            nombreDeLiens = 17
            print(nombreDeLiens)
        else:
            print(nombreDeLiens)
        
        comptePour12Liens = 0
        while comptePour12Liens < nombreDeLiens:
            link = (links[comptePour12Liens].get_attribute('href'))
            listeDeLiensNonClean.append(link)
            comptePour12Liens = comptePour12Liens + 1

        print(listeDeLiensNonClean)
        print(len(listeDeLiensNonClean))
        
        # on nettoye les 2 premiers liens de la base de donnée car il ne sont pas utiles
        cleanLinks = []
        compteurLink = 2

        while compteurLink < nombreDeLiens:
            listeDeLiensClean.append(listeDeLiensNonClean[compteurLink])
            compteurLink = compteurLink +1
    
        if (listeDeLiensClean == 0):
            print(Fore.RED + "problem occured with xpath...")
            print(Style.RESET_ALL)
            try:
                onetrust = driver.find_element(By.XPATH,'//*[@id="onetrust-reject-all-handler"]').click()
            except NoSuchElementException:
                pass
            timeSleeper()
            print("Cookie validé")
            links = driver.find_elements(By.CLASS_NAME,'jcs-JobTitle')
            nombreDeLiens = len(links)
            if (nombreDeLiens < 4):
                print(urlParent)
                recapcha(driver)
                timeSleeper()
                links = driver.find_elements(By.XPATH,'/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[4]/div/ul/li/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[1]/h2')
                nombreDeLiens = len(links)
            # commenté cette ligne elif si vous voulez scrapper plus de 10jobs
            elif (nombreDeLiens > 17):
                nombreDeLiens = 17
                print(nombreDeLiens)
            else:
                print(nombreDeLiens)
            
            comptePour12Liens = 0
            while comptePour12Liens < nombreDeLiens:
                link = (links[comptePour12Liens].get_attribute('href'))
                listeDeLiensNonClean.append(link)
                comptePour12Liens = comptePour12Liens + 1

            print(listeDeLiensNonClean)
            print(len(listeDeLiensNonClean))
            
            # on nettoye les 2 premiers liens de la base de donnée car il ne sont pas utiles
            cleanLinks = []
            compteurLink = 2

            while compteurLink < nombreDeLiens:
                listeDeLiensClean.append(listeDeLiensNonClean[compteurLink])
                compteurLink = compteurLink +1

        print(len(listeDeLiensClean))
        # print(listeDeLiensClean)

        # input d'attente facultatif
        # input("//////////// RESULTAT A L'ECRAN \n")


        for scrappingUrl in listeDeLiensClean:
            driver.get(scrappingUrl)
            print('waiting 2sec...')
            timeSleeper()
            recapcha(driver)

            # stockage de la date actuelle
            date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
            print(date)

            # récupération de l'url
            url = scrappingUrl
            print(url)

            # récupération du titre
            titre = driver.find_elements(By.XPATH,'//div[contains(@class, "jobsearch-JobInfoHeader-title-container")]//h1[contains(@class, "jobsearch-JobInfoHeader-title")]')
            for titreLien in titre: 
                titre = (titreLien.get_attribute('innerHTML'))
                if titre == '[]':
                    print(Fore.RED + 'titre bugged, stopping the loop')
                    titreLien[titre] = None
                    offresIndeed.append(make_a_dict_of_valuesV2(date,url,titre,ville,contrat,description,salary,metier,statut,secteur,experience,lieux,categorie))

                    with open(f"{directory}/{forJson}.json", "wb") as writeJSON:
                        jsStr = json.dumps(offresIndeed)
                        # the decode() needed because we need to convert it to binary
                        writeJSON.write(jsStr.encode('utf-8')) 
                        print ('end')

                    print(Style.RESET_ALL)
                    break
            print(titre)
            metier = titre
            
            # récupération de la ville
            
            try:
                ville = driver.find_element(By.XPATH,'//*[@id="viewJobSSRRoot"]/div[2]/div/div[3]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div')
                ville = ville.text
            except InvalidSelectorException:
                try:
                    ville = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div[3]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div')
                    ville = ville.text
                except InvalidSelectorException:
                    ville = driver.find_element(By.CLASS_NAME,'.icl-u-textColor--secondary > div:nth-child(2) > div:nth-child(1)')
                    ville = ville.text
            except NoSuchElementException:  #spelling error making this code not work as expected
                try:
                    ville = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div[3]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div')
                    ville = ville.text
                except InvalidSelectorException:
                    ville = driver.find_element(By.CLASS_NAME,'.icl-u-textColor--secondary > div:nth-child(2) > div:nth-child(1)')
                    ville = ville.text
                except NoSuchElementException:
                    try:
                        ville = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[3]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]')
                        ville = ville.text
                    except InvalidSelectorException:
                        ville = driver.find_element(By.CLASS_NAME,'.icl-u-textColor--secondary > div:nth-child(2) > div:nth-child(1)')
                        ville = ville.text
                    except NoSuchElementException:
                        try:
                            ville = driver.find_element(By.CLASS_NAME,'.icl-u-textColor--secondary > div:nth-child(2) > div:nth-child(1)')
                            ville = ville.text
                        except NoSuchElementException:
                            ville = 'France'
                            pass
                        except InvalidSelectorException:
                            try:
                                ville = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div[3]/div/div/div[1]/div[1]/div[3]/div[1]/div[2]/div/div/div/div[2]/div')
                                ville = ville.text
                            except NoSuchElementException:
                                ville = 'France'
                        
            hours = datetime.today().strftime('%H %S%M')
            ville = str(ville) + ' ' + str(hours) + ' °'
            print(Fore.GREEN + ville + Style.RESET_ALL)

            # récupération de la description
            try:
                description = driver.find_element(By.XPATH,'//div[contains(@id, "jobDescriptionText")]')
                description = description.text
            except NoSuchElementException:  #spelling error making this code not work as expected
                try:
                    description = driver.find_element(By.ID,'jobDescriptionText')
                    description = description.text
                except NoSuchElementException:
                    description = "contactez l'employeur"
                    pass  
            print(description)
            timeSleeper()

            # récupération du salaire
            try:
                salary = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div[2]/div[1]/div/span[1]')
                salary = salary.text
            except NoSuchElementException:
                salary = 'A définir'
                print(Fore.RED + 'bug xpath salary')
                print(Style.RESET_ALL)
                pass
            print(salary)

            # récupération du type de contrat
            try:
                contrat = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div[2]/div[1]/div/span[2]')
                contrat = contrat.text
            except NoSuchElementException:  #spelling error making this code not work as expected
                contrat = "CDI"
                pass
            print(contrat)
            statut = contrat

            # récupération du secteur
            try:
                secteur = titre.text.split()[0]
            except AttributeError:
                secteur = titre
            else:
                secteur = titre.text.split()[0]
            experience = "Tous niveaux d'expérience acceptés"
            
            
            print(Fore.RED + str(categorie) + Style.RESET_ALL)
            offresIndeed.append(make_a_dict_of_valuesV2(date,url,titre,ville,contrat,description,salary,metier,statut,secteur,experience,lieux,categorie))

    with open(f"{directory}/{forJson}--{getLocation}.json", "wb") as writeJSON:
        jsStr = json.dumps(offresIndeed)
        # the decode() needed because we need to convert it to binary
        writeJSON.write(jsStr.encode('utf-8')) 
        print ('end')

    print(Fore.LIGHTMAGENTA_EX + str(forJson) + Style.RESET_ALL)
    compteurBouclesListeDates = compteurBouclesListeDates +1
    print(Fore.YELLOW + str(compteurBouclesListeDates) + Style.RESET_ALL)
    driver.quit()

# libération mémoire
del listeJob
del listeDepartement
del listeLieu