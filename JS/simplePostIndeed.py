
from headers.headerPyMonGo import *

try:
	client = MongoClient("mongodb://192.168.1.174:27017/")
	print("Connected successfully!!!")
except:
	print("Could not connect to MongoDB")

J = input("Tapez le jour désiré de 01 à 31: \n")
M = input("Tapez le mois désiré de 01 à 12: \n")
date = J+M

pathStockDesJsons = f"C:/Users/admin/Desktop/DeskCeption/Scripts/ScriptPosteurIndeed/stockageOffreIndeed{date}"
os.chdir(pathStockDesJsons)

listeDesJsonStockes = [f for f in listdir(pathStockDesJsons) if isfile(join(pathStockDesJsons, f))]

# gestions des doublons
# doublon = []
# for i in listeDesJsonStockes:
#     z = i.split('--')
#     jobDep = z[1] + z[2]
#     doublon.append(jobDep)
#     # print(doublon)
#     if doublon.count(jobDep) > 1:
#         print(Fore.YELLOW + i + Style.RESET_ALL)
#         doublon.remove(jobDep)

# print(Fore.RED + str(doublon) + Style.RESET_ALL)
# print(listeDesJsonStockes)


# c = 0
# while c < len(listeDesJsonStockes):
#     jsonCleaned = listeDesJsonStockes[c].split('--')
#     jsonCleaned = jsonCleaned[1] + jsonCleaned[2]
#     if jsonCleaned in doublon:
#         listeDesJsonStockes.remove(listeDesJsonStockes[c])
#         doublon.remove(jsonCleaned)
#     c = c + 1

# print(Fore.RED + str(doublon) + Style.RESET_ALL)
# print(listeDesJsonStockes)

print(Fore.BLUE + str(listeDesJsonStockes) + Style.RESET_ALL)
# print(listeDesJsonStockes[0])
nombreDeBoucles = len(listeDesJsonStockes)


compteurBoucles = 0
db = client.VRio

while compteurBoucles < nombreDeBoucles:
    col = db["regionjob_annonce"]
    col.drop()
    col = db["regionjob_annonce"]
    with open(f"{listeDesJsonStockes[compteurBoucles]}") as file: 
        file_data = json.load(file) 

        try:
            col.insert_many(file_data)
        except:
            try:
                col.insert_one(file_data)
            except TypeError:
                print(Fore.RED + "La stack est vide")
                print(Style.RESET_ALL)
                with open(f'../stackVide/{listeDesJsonStockes[compteurBoucles]}.txt', encoding='utf-8', mode='w') as file:
                    file.write(f"{listeDesJsonStockes[compteurBoucles]}")
    # nombrePoste = 'test'
    try:
        nombrePoste = col.count('regionjob_annonce')
        print(Fore.BLUE + str(nombrePoste) + 'de postes dans la stack' + Style.RESET_ALL)
    except TypeError:
        pass
    # print(str(nombrePoste)+ 'postes')
    print(Fore.YELLOW + listeDesJsonStockes[compteurBoucles])
    print(Style.RESET_ALL)
    # posteurJsPath = "C:/Users/admin/Desktop/indeed/PosteurJS"
    # os.chdir(posteurJsPath)
    # os.system('start cmd /c "npm start"') 

    launchParamiko = "C:/Users/admin/Desktop/DeskCeption/Scripts/ScriptPosteurIndeed"
    os.chdir(launchParamiko)
    # test 
    os.system('start cmd /k "py .\connectSSH.py"')

    # time.sleep(750)
    print(Fore.RED + "A l'utilisation de mon script soyez extrêmement vigilant à ne pas modifier la commande Taskill...")
    input("Press enter when posting is finished : ...\n")
    print(Style.RESET_ALL)

    # Ne pas toucher
    os.system("taskkill /f /im cmd.exe /t")
    # Ne pas toucher

    os.chdir(pathStockDesJsons)

    compteurPlus = input("When you are ready to continue press enter, if you want to skip the next one press 2")
    if compteurPlus == '2':
        compteurBoucles = compteurBoucles + 2
    else:
        compteurBoucles = compteurBoucles + 1
        