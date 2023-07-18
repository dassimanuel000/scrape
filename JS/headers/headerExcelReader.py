import os
import os.path
import pandas as pd
import colorama

from calendar import c
from datetime import datetime
from os.path import exists
from colorama import Fore
from colorama import Style
from urllib.parse import ParseResult, urlparse
from datetime import datetime
from openpyxl import load_workbook

# initialisation colorama
colorama.init()

# stockage du path du script  
currentDir = os.path.abspath(os.getcwd())
currentDir = currentDir.replace('\\', '/')
print(currentDir)

# Fonctions utilisé pour créer des listes à partir de l'excel

# création de liste
def make_a_converted_list_job(date):
    listeDesJobsDeCetteDate = list(df1[df1['Date de Post'] == f'{date}']['Profession 1'])
    return listeDesJobsDeCetteDate

def make_a_converted_list_departement(date):
    listeDesDptmntsDeCetteDate = list(df1[df1['Date de Post'] == f'{date}']['Département / GV'])
    return listeDesDptmntsDeCetteDate

def make_a_converted_list_lieu_precis(date):
    listeDesDptmntsDeCetteDate = list(df1[df1['Date de Post'] == f'{date}']['Lieu Très Précis'])
    return listeDesDptmntsDeCetteDate

def make_a_converted_list_categorie(date):
    listeDesDptmntsDeCetteDate = list(df1[df1['Date de Post'] == f'{date}']['Catégories'])
    return listeDesDptmntsDeCetteDate

def make_a_converted_list_job_null():
    listeDesJobsDeCetteDate = list(df1[df1['Date de Post'].isnull()]['Profession 1'])
    return listeDesJobsDeCetteDate

def make_a_converted_list_departemen_null():
    listeDesDptmntsDeCetteDate = list(df1[df1['Date de Post'].isnull()]['Département / GV'])
    return listeDesDptmntsDeCetteDate

def make_a_converted_list_lieu_precis_null():
    listeDesDptmntsDeCetteDate = list(df1[df1['Date de Post'].isnull()]['Lieu Très Précis'])
    return listeDesDptmntsDeCetteDate

def make_a_converted_list_categorie_null():
    listeDesDptmntsDeCetteDate = list(df1[df1['Date de Post'].isnull()]['Catégories'])
    return listeDesDptmntsDeCetteDate

def make_a_converted_list_job_trait():
    listeDesJobsDeCetteDate = list(df1[df1['Date de Post'] == '-']['Profession 1'])
    return listeDesJobsDeCetteDate

def make_a_converted_list_departemen_trait():
    listeDesDptmntsDeCetteDate = list(df1[df1['Date de Post'] == '-']['Département / GV'])
    return listeDesDptmntsDeCetteDate

def make_a_converted_list_lieu_precis_trait():
    listeDesDptmntsDeCetteDate = list(df1[df1['Date de Post'] == '-']['Lieu Très Précis'])
    return listeDesDptmntsDeCetteDate

def make_a_converted_list_categorie_trait():
    listeDesDptmntsDeCetteDate = list(df1[df1['Date de Post'] == '-']['Catégories'])
    return listeDesDptmntsDeCetteDate

# clean des variables a l'intérieur de la boucle
def make_better_job(i):
    try:
        goodListeJob = listeJob[i].split('/')
    except AttributeError:
        goodListeJob = listeJob[i]
    try:
        noSlashJob = goodListeJob[0]
    except TypeError:
        noSlashJob = goodListeJob
    return noSlashJob

def make_better_dep(i):
    try:
        goodListeDepartement = listeDepartement[i].replace(' / ', '/').replace(' /', '/').replace('/ ','/').split('/')
        noSlashDepartement = goodListeDepartement[0]
        goodSlashDepartement = noSlashDepartement.split(',')
        noVirguleDepartement = goodSlashDepartement[0]
    except AttributeError:
        noVirguleDepartement = listeDepartement[i]
    return noVirguleDepartement

# parsing de l'url pour récupérer le titre du job et la ville du job a scrapé
def parse_url(url):
    urlParse = url.split("?")
    urlParse = urlParse[1].split("&")
    urlTitreJob = urlParse[0].split("=")
    urlVilleJob = urlParse[1].split("=")
    urlTitreJob = urlTitreJob[1]
    urlVilleJob = urlVilleJob[1]
    urlFinal = urlTitreJob + "--" + urlVilleJob
    return urlFinal

# écriture du json de manière ordonnée
def write_my_json(url, i):
    writeO = '00'
    countToWrite = str(i)
    if i < 10:
        countToWrite = writeO + str(i)
    elif i < 100:
        countToWrite = '0' + str(i)
    forJson = str(countToWrite) + "--" + url
    return forJson

# connection à l'excel préalablement téléchargé
df = pd.read_excel (r'Populations.xlsx', parse_dates=['Date de Post'])
# récupération des 7 premières colonnes verticales
df1 = df.iloc[: , :9] 

# récupération de la date dans l'excel permettant la création des listes de dates désirées
J = input("Tapez le jour désiré de 01 à 31: \n")
M = input("Tapez le mois désiré de 01 à 12: \n")
date = f'2022-{M}-{J} 00:00:00'
# Dossier à creer
directory = "stockageOffreIndeed" + J + M

# mode
mode = 0o666

# Path
path = os.path.join(currentDir, directory)

# Create the directory
try:
    os.mkdir(path, mode)
    print("Directory '% s' created" % directory)
except FileExistsError:
    print('Dossier déja existant')

# Date non null = ancienne stack / stack avec dates
listeJob = make_a_converted_list_job(date)
listeDepartement = make_a_converted_list_departement(date)
listeLieu = make_a_converted_list_lieu_precis(date)
listeCategorie = make_a_converted_list_categorie(date)
print(Fore.CYAN + f'Creation de piles json pour les stack datant du {date}' + Style.RESET_ALL)

# Date null = nouvelles stacks
# listeJob = make_a_converted_list_job_null()
# listeDepartement = make_a_converted_list_departemen_null()
# listeLieu = make_a_converted_list_lieu_precis_null()
# listeCategorie = make_a_converted_list_categorie_null()
# print(Fore.CYAN + 'Creation de piles json pour les nouvelles stack' + Style.RESET_ALL)

# Date - = stack bugué
# listeJob = make_a_converted_list_job_trait()
# listeDepartement = make_a_converted_list_departemen_trait()
# listeLieu = make_a_converted_list_lieu_precis_trait()
# listeCategorie = make_a_converted_list_categorie_trait()
# print(Fore.CYAN + f'Creation de piles json pour les stack ayant des traits' + Style.RESET_ALL)