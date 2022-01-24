const utils = require('./utils');
const mongoose = require('mongoose');
const annonce = require('./annonce');

const scrapping = {
    async scrapeCurrentPage(page) { //Gives us a table of pages in which we scrape
        let arr = [];
       let counter = 0;
       let table = [];
        async function recall(){
        
        await page.setDefaultNavigationTimeout(0);
        if (counter===0){
        try {
            await utils.delay(2000);
            await page.click('div#onetrust-button-group > button#onetrust-accept-btn-handler');
            await utils.delay(1000);
        } catch {
            console.log('failed cookies');
        }
        }
        await utils.delay(2000);
        let hrefs = await page.$$eval('.container-result > div > a', as => as.map(a => a.href));
       table = hrefs;
        } 
        while(counter<=0){
            console.log(counter);
            let contract = 101888; //CDI 
                // https://www.apec.fr/candidat/recherche-emploi.html/emploi?fonctions=101832&typesContrat=${contract}&page=${counter} cdi adminisratif
            // https://www.apec.fr/candidat/recherche-emploi.html/emploi?typesContrat=${contract}&page=${counter} cdi
            // https://www.apec.fr/candidat/recherche-emploi.html/emploi?motsCles=secretaire-assistante&page=${counter}
            // https://www.apec.fr/candidat/recherche-emploi.html/emploi?motsCles=secretaire%20general&page=1
            // https://www.apec.fr/candidat/recherche-emploi.html/emploi?motsCles=developpeur&page1=&page=0
            //https://www.apec.fr/candidat/recherche-emploi.html/emploi?typesContrat=101888&page=${counter}&motsCles=Gestionnaire%20de%20paie
            //https://www.apec.fr/candidat/recherche-emploi.html/emploi?typesContrat=101888&page=${counter}&motsCles=%22Secr%C3%A9taire%22
            url = `https://www.apec.fr/candidat/recherche-emploi.html/emploi?typesContrat=101888&motsCles=Conseiller%20de%20vente%20Sables%20D%27Olonne&sortsType=SCORE&page=${counter}`;
                await page.goto(url, {waitUntil: 'domcontentloaded', timeout: 300000});
                await page.setDefaultNavigationTimeout(0);
                console.log(`Navigating to ${url}...`);
                await recall();
                await arr.push(table);
                table = [];
            ++counter;
        }

            return arr; 
  },
  async scrapeAnnoncePage(page, url) { // Enables us to scrape the pages from the file
        let dataObj = {};
        await page.setDefaultNavigationTimeout(0); // on désactive le timeout de 30 secondes
        await page.goto(url);
        
        try { // Check for cookie pages click on new pages
            await page.waitForSelector('button#onetrust-accept-btn-handler');
            await utils.delay(2000);
            await page.click('button#onetrust-accept-btn-handler');
            await utils.delay(2000);
        } catch {
            console.log('failed cookies');
        }
        
        try {
            dataObj['date'] = new Date().toISOString(); // date dans un format facile à lire et reconvertir pour avoir un suivi
            dataObj['url'] = await page.url(); // stockage url de l'annonce
            dataObj['titre'] = await page.$eval('.card-offer__text > h2', text => text.textContent); // stockage du titre de l'annonce
            let activite = await page.$$eval('.card-offer__text > .details-offer-list > li', async catlinks => { // on ne peux pas différencier les activiées par classe css donc on récupére la liste et on selectionne la case, on teste deux cases
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
            
            let postdate = await page.$$eval('.mb-10 > div > .date-offre', async catlinks => { // on ne peux pas différencier les activiées par classe css donc on récupére la liste et on selectionne la case, on teste deux cases
                // Extract the links from the data
                catlinks = await catlinks.map(el => el.textContent);
                return catlinks;
            });

            
            dataObj['postTime'] = postdate[1].replace(/[^\d]/g, "")
            let tmpText = await page.$eval('.col-lg-8 > .details-post', text => text.innerText);
            tmpText = tmpText.split("[\\r\\n]+");
            dataObj['description'] = tmpText[0];

            let moredata = await page.$$eval('.details-post > span', async catlinks => { // on ne peux pas différencier les activiées par classe css donc on récupére la liste et on selectionne la case, on teste deux cases
                // Extract the links from the data
                catlinks = await catlinks.map(el => el.textContent);
                return catlinks;
            });
            dataObj['salary'] = moredata[0];
            dataObj['experience'] = moredata[2];
            dataObj['metier'] = moredata[3];
            dataObj['statut'] = moredata[4];
            dataObj['secteur'] = moredata[6];

            return (dataObj);
        }
        catch(err) {
            console.log(err);
            await page.close();
            return (dataObj);
        }
}, 
};

module.exports = scrapping;