
from headers.headerPyMonGo import *
import subprocess
import sys

try:
	client = MongoClient("mongodb://localhost:27017/")
	print("Connected successfully!!!")
except:
	print("Could not connect to MongoDB")

J = sys.argv[1]
M = sys.argv[2]
date = J+"-"+M
#date = "19-03"
pathStockDesJsons = f"/home/jeremy/Documents/ScriptsRio/ScriptsRio/ScriptePosteurTalent/stockageOffres{date}"
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
db = client.VSuperOrdiTalent

while compteurBoucles < nombreDeBoucles:
    if compteurBoucles > 0:
        os.remove(listeDesJsonStockes[compteurBoucles - 1])
    print(Fore.CYAN + str(compteurBoucles + 1)+ 'e boucle dans le dossier' + Style.RESET_ALL)
    col = db["regionjob_annonce"]
    col.drop()
    col = db["regionjob_annonce"]
    with open(f"{listeDesJsonStockes[compteurBoucles]}", encoding='utf-8') as file: 
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

    # launch posteur python complexe
    launchParamiko = "/home/jeremy/Documents/ScriptsRio/ScriptsRio/ScriptePosteurTalent/"
    os.chdir(launchParamiko)
    # 3Posteur
    cmd = ['python3.10', '4posteurWithNoHead.py']
    subprocess.Popen(cmd).wait()
    os.chdir(pathStockDesJsons)
    compteurBoucles = compteurBoucles + 1
