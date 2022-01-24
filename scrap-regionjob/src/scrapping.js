const utils = require('./utils');
const mongoose = require('mongoose');
const annonce = require('./annonce');

async function doclean(str, bool) {
    let cleanstr;

    try {
    if (bool) {
        str = str.split(":");
        cleanstr = str[1].replace(/(\r\n|\n|\r)/gm, "");
        cleanstr = cleanstr.replace(/  +/g, ' ');
    } else if (!bool) {
        cleanstr = str.replace(/(\r\n|\n|\r)/gm, "");
        cleanstr = cleanstr.replace(/  +/g, ' ');
    }
    return cleanstr;
    } catch (err) {
        console.log("bad str", str);
        return str;
    }
}

const scrapping = {
    async scrapeCurrentPage(page) { //Gives us a table of pages in which we scrape
        let arr = [];
       let counter = 1;
       let table = [];
        async function recall(){
        
        await page.setDefaultNavigationTimeout(0);
        if (counter===0){
        try {
            await page.waitForSelector('button#hw-cc-notice-accept-btn');
            await utils.delay(2000);
            await page.click('button#hw-cc-notice-accept-btn');
            await utils.delay(1000);
        } catch {
            console.log('failed cookies');
        }
        }
        await utils.delay(2000);
        let hrefs = await page.$$eval('h3 > a', as => as.map(a => a.href));
       table = hrefs;
        } 
        while(counter<=3){
            console.log(counter);
            //employé polyvalent
            //secrétaire
            let keywordToHTML = "secrétaire";
            keywordToHTML = await keywordToHTML.replace(/ /g, '%20');
                url = `https://www.regionsjob.com/emploi/recherche?k=${keywordToHTML}&p=${counter}&mode=pagination`;
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
        await page.goto(url, {waitUntil: 'domcontentloaded', timeout: 300000});
        await page.setDefaultNavigationTimeout(0); // on désactive le timeout de 30 secondes
        
        try {
            await page.waitForSelector('button#hw-cc-notice-accept-btn');
            await utils.delay(2000);
            await page.click('button#hw-cc-notice-accept-btn');
            await utils.delay(1000);
        } catch {
            console.log('failed cookies');
        }
        
        try {
            dataObj['date'] = new Date().toISOString(); // date dans un format facile à lire et reconvertir pour avoir un suivi
            dataObj['url'] = await page.url(); // stockage url de l'annonce
            dataObj['titre'] = await page.$eval('h1', text => text.textContent); // stockage du titre de l'annonce
            let activite = await page.$$eval('section[class="content retrait modal"] > ul > li', async catlinks => {
                // Extract the links from the data
                catlinks = await catlinks.map(el => el.textContent);
                return catlinks;
            });
            let metier = activite[0];
            dataObj['metier'] = await doclean(metier, true);
            let secteur = activite[1];
            dataObj['secteur'] = await doclean(secteur, true);
            let city = activite[2];
            dataObj['ville'] = await doclean(city, true);
            let exp = activite[3];
            exp = exp.substr(33);
            dataObj['experience'] = await doclean(exp, false);
            let contract = activite[4];
            contract = contract.substr(31);
            dataObj['contrat'] = await doclean(contract, false);
            let salary = activite[6];
            dataObj['salary'] = await doclean(salary, true);
            
            let time = await page.$eval('.retrait > span', text => text.textContent) // stockage du titre de l'annonce
            const datePattern = /(\d{1,2})\/(\d{1,2})\/(\d{4})/;
            time = datePattern.exec(time);
            dataObj['postTime'] = time[0];

            dataObj['description'] = await page.$eval('section[class="content modal"]', text => text.innerText);

            console.log("DATAOBJ", dataObj);

            return (dataObj);
        }
        catch(err) {
            console.log(err);
            await page.close();
            return (0);
        }
}, 
};

module.exports = scrapping;
