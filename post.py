# Python program to explain os.mkdir() method
from itertools import count
from operator import mod
from os import listdir
from os.path import isfile, join
from pprint import pprint
import json
import time
#from typing import  Literal 
import colorama
from colorama import Fore
from colorama import Style
from pymongo import MongoClient
from selenium.webdriver.common.alert import Alert 
from cgi import test
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

# importing os module
import os

colorama.init()
    
"""
try:
	client = MongoClient("mongodb://192.168.1.174:27017/")
	print("Connected successfully!!!")
except:
	print("Could not connect to MongoDB")

J = input("Tapez le jour désiré de 01 à 31: \n")
M = input("Tapez le mois désiré de 01 à 12: \n")
date = J+M
"""
pathStockDesJsons = f"C:/Users/admin/Documents/DEV TEST/Amelioration/job_indeed_linkedin"
os.chdir(pathStockDesJsons)
listeDesJsonStockes = [f for f in listdir(pathStockDesJsons) if isfile(join(pathStockDesJsons, f))]

# print(listeDesJsonStockes[0])
nombreDeBoucles = len(listeDesJsonStockes)
# arrêté à 6 Préparatrice de commande
compteurBoucles = 0
#db = client.V2

while compteurBoucles < nombreDeBoucles:
    with open(f"{listeDesJsonStockes[compteurBoucles]}") as file: 
        file_data = json.load(file) 

        try:
            print(file_data)
            print("--------------------------------------------------------------------------------------------------------")
        except:
            with open(f'./stackVide/{listeDesJsonStockes[compteurBoucles]}.txt', encoding='utf-8', mode='w') as file:
                file.write(f"{listeDesJsonStockes[compteurBoucles]}")
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

    print(Fore.YELLOW + listeDesJsonStockes[compteurBoucles])
    """print(Style.RESET_ALL)
    # posteurJsPath = "C:/Users/admin/Desktop/indeed/PosteurJS"
    # os.chdir(posteurJsPath)
    # os.system('start cmd /c "npm start"') 

    launchParamiko = "C:/Users/admin/Desktop/indeed"
    os.chdir(launchParamiko)
    # test 
    os.system('start cmd /k "py .\connectSSH.py"')


    # time.sleep(750)
    print(Fore.RED + "A l'utilisation de mon script soyez extrêmement vigilant à ne pas modifier la commande Taskill...")
    input("Press enter when posting is finished : ...\n")
    print(Style.RESET_ALL)

    # Ne pas toucher
    os.system("taskkill /f /im cmd.exe /t")"""
    # Ne pas toucher

    os.chdir(pathStockDesJsons)

    input("When you are ready to continue press enter")
    compteurBoucles = compteurBoucles + 1