const mongoose = require('mongoose');
const annonce = require('./annonce');

async function delay(time) { // fonction pour attendre
    return new Promise(function(resolve) { 
        setTimeout(resolve, time)
    });
 }

let pageNumber = 0;
const scraperObject = { // script de scrapping
    url: 'https://www.apec.fr/candidat/recherche-emploi.html/emploi?typesContrat=101888', //cdi
    //url: 'https://www.apec.fr/candidat/recherche-emploi.html/emploi?typesContrat=101887', //cdd

    async scraper(browser) {
        let page = await browser.newPage();
        console.log(`Navigating to ${this.url}...`);
        await page.goto(this.url);
        await page.waitForSelector('.container-result'); // selection du champs qui servira de parent au recherche suivante
        pageNumber++;

        await scrapeCurrentPage(); // appel à la fonction de récupération des liens d'annonce
        // Wait for the required DOM to be rendered
        async function scrapeCurrentPage(){
        page.waitForNavigation({ waitUntil: 'networkidle2' });
        await page.setDefaultNavigationTimeout(0);

        // Get the link to all the required books
        await delay(4427);

        let date = 0;
        if (date != 0 && date == "03/11/2021") //20/10
        return 0;//break;

        const hrefs = await page.$$eval('.container-result > div > a', as => as.map(a => a.href)); // selection de tout les liens de la page
        console.log("hrefs: ", hrefs);
        let arr = [];
        hrefs.forEach(element => {
            if(element != null) {
                let regexbis = "https://www.apec.fr/candidat/recherche-emploi.html/emploi/detail-offre"; // vérification que les liens sont des annonces
                if (element.match(regexbis)) {
                    arr.push(element);
                }
            } else {
                console.log("arr is null");
            }
            
        });

      //  console.log("arr: ", arr);

        await delay(3000); // on attend 3 secondes
        let getProfileData = (urls) => new Promise(async(resolve, reject) => { // fonction pour récupérer les données de l'annonce
            let dataObj = {};
            let profPage = await browser.newPage(); // on ouvre une nouvelle page
            await profPage.setDefaultNavigationTimeout(0); // on désactive le timeout de 30 secondes
            await profPage.goto(urls, {
                waitUntil: 'networkidle2', // on navigue jusqu'a l'url en attendant que la page finisse de charger avec 300 secondes de timeout
                timeout: 300000
            });

            await profPage.waitForSelector('.card-body');
            try {
                dataObj['date'] = new Date().toISOString(); // date dans un format facile à lire et reconvertir pour avoir un suivi
                dataObj['url'] = await profPage.url(); // stockage url de l'annonce
                dataObj['titre'] = await profPage.$eval('.card-offer__text > h2', text => text.textContent); // stockage du titre de l'annonce
                let activite = await profPage.$$eval('.card-offer__text > .details-offer-list > li', async catlinks => { // on ne peux pas différencier les activiées par classe css donc on récupére la liste et on selectionne la case, on teste deux cases
                    // Extract the links from the data
                    catlinks = await catlinks.map(el => el.textContent);
                    return catlinks;
                });
                
               // const activitesplit = String(activite[0]).split('\n');
             //   console.log("activite", activite);

                dataObj['compagny'] = activite[0];
                dataObj['contrat'] = activite[1];
                
                try {
                dataObj['ville'] = activite[2];
                } catch (err) {console.log("pas d'activité");}
                
                let postdate = await profPage.$$eval('.mb-10 > div > .date-offre', async catlinks => { // on ne peux pas différencier les activiées par classe css donc on récupére la liste et on selectionne la case, on teste deux cases
                    // Extract the links from the data
                    catlinks = await catlinks.map(el => el.textContent);
                    return catlinks;
                });

                
                dataObj['postTime'] = postdate[1].replace(/[^\d]/g, "")
                dataObj['description'] = await profPage.$eval('.col-lg-8 > .details-post', text => text.textContent);

                let moredata = await profPage.$$eval('.details-post > span', async catlinks => { // on ne peux pas différencier les activiées par classe css donc on récupére la liste et on selectionne la case, on teste deux cases
                    // Extract the links from the data
                    catlinks = await catlinks.map(el => el.textContent);
                    return catlinks;
                });
                dataObj['salary'] = moredata[0];
                dataObj['experience'] = moredata[2];
                dataObj['metier'] = moredata[3];
                dataObj['statut'] = moredata[4];
                dataObj['secteur'] = moredata[6];

                resolve(dataObj);
                //return (dataObj);
                await profPage.close();
            }
            catch(err) {
                console.log(err);
                resolve("0");
                await profPage.close();
            }
        });
        //here go to the main scrapping function
        for (let counter = 0; counter < arr.length; counter++) { // on loop sur les liens d'annonce de la page
            console.log("final counter", arr[counter]);
                let dataObj = await getProfileData(arr[counter]); // on récupère les donnnées
              //  console.log("complete OBJ", dataObj);

                await mongoose.connect('mongodb://localhost/apec', { // on envois les données sur mongodb
                    useNewUrlParser: true,
                    useUnifiedTopology: true,
                    //useFindAndModify: false,
                    //useCreateIndex: true
                });
                
                    let thdata = new annonce();
                    thdata.date = dataObj['date'];
                    thdata.url = dataObj['url'];
                    thdata.titre = dataObj['titre'];
                    thdata.company = dataObj['company'];
                    thdata.contrat = dataObj['contrat'];
                    thdata.ville = dataObj['ville'];
                    thdata.activite = dataObj['activite'];
                    thdata.description = dataObj['description'];
                    thdata.posttime = dataObj['posttime'];
                    thdata.salary = dataObj['salary'];
                    thdata.metier = dataObj['metier'];
                    thdata.statut = dataObj['statut'];
                    thdata.secteur = dataObj['secteur'];
                    thdata.experience = dataObj['experience'];
                    thdata.save(function (err) {
                        if (err) console.log("INSERTION FAILED", err);
                        else { // saved!
                            console.log("SAVED");
                        }
                  });
            }
            // You are going to check if this button exist first, so you know if there really is a next page.
            
            if (pageNumber <= 1038) { //config page count max here 1150
                let nextButton = "https://www.apec.fr/candidat/recherche-emploi.html/emploi?typesContrat=101888&page=" + pageNumber; //cdi 1038
              //  let nextButton = "https://www.apec.fr/candidat/recherche-emploi.html/emploi?typesContrat=101887&page=" + pageNumber; //cdd

                pageNumber++;
               // console.log(nextButton);
                await delay(3000);
                await page.goto(nextButton);
                console.log("nextButton", nextButton);
                return await scrapeCurrentPage(); // Call this function recursively
            } else {
                await page.close();
                return scrapedCatData; }
            
        }
    }
}

module.exports = scraperObject;