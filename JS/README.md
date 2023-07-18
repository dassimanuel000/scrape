Version 1.00 : 
CLEMENT Rio - Scrap de indeed avec diverses implémentations. 
Import de os/os.path pour vérification de l'existense du dossier json.

Comment utiliser mes scripts : 
se réferer à headerExcelReader 
Choisir à la fin au niveau des lignes 143 les stacks voulues.

Pour une date précise décommenté a partir de dates non null.
Pour de nouvelles stacks ou la date n'est pas inscripte; décommenté à partir de dates null.
Pour les tirets décommenté à partir de dates.

Pour un scrappage en masse : 
py 0ComplexeScrap

Une date vous sera demandé : 
Choisissez la date des offres que vous voulez récuperez en suivant le command prompt demandez par le script

Une fois les offres scrappés.
Faites : 
py 2posteur

Les offres vont s'envoyer de manière automatiques sur le site. N'hésitez pas à controler. Un 
bug récurrent vient au moment de la publication. il faut cliquez sur publier 2 fois. (point à améliorer)
Vous pouvez laisser l'ordi allumé et il s'occupera de tout.

Vous avez aussi py OneScrap pour scrapper une seule offre. 
Et vous pouvez aussi utiliser py simplePostIndeed pour envoyer les offres une à une qui est plus rapide via le script js.



python3.10 3posteurHeadless.py
cd /home/jeremy/Documents/ScriptsRio/ScriptsRio/ScriptePosteurTS/src
node index.js
cd ..
python3.10 3posteurHeadless.py
