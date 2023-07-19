const utils = require('./utils');
const xlsxFile = require('read-excel-file/node');
const prompt = require('prompt-sync')();
let counter = 0;
let cats = '';
let places = ''
//Urls des différents sites à scrap
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
    if (cleanstr=="undefined"){
        cleanstr = '';
    }
    return cleanstr;
    } catch (err) {
        console.log("bad str", str);
        return String(str).split('  ').join('').split('\n').join('');
    }
}
apecUrl = `https://www.apec.fr/candidat.html`;
franceemploiURL = 'https://www.france-emploi.com/recherche-emploi/?q=';
helloworkURL = 'https://www.hellowork.com/fr-fr';
urlPe = `https://candidat.pole-emploi.fr/offres/recherche?emission=1&lieux=19031&motsCles=Adjoint+De+Direction&offresPartenaires=true&range=0-19&rayon=30&tri=0`;
teepyjobURL = 'https://teepy-job.com/offres-emploi/',
jobup = `https://www.jobup.ch/fr/emplois/`
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
    if (cleanstr=="undefined"){
        cleanstr = '';
    }
    return cleanstr;
    } catch (err) {
        console.log("bad str", str);
        return String(str).split('  ').join('').split('\n').join('');
    }
}

const scrapping = {

async scrapeLinkPagejobup(page,i,y) { //Gives us a table of pages in which we scrape
    //base variables iterator and variables to store the data we'll need for Hellowork
    let arr = [];
    let counter = 1;
    let table = [];
    let metier = '';
    let region = '';
    let teleUrl;
    /*
    let choice = prompt("want to use Scrap Hello Work ? yes or no \n");
    if(choice == "no"||choice=='n'){
        return arr;
    }
    */
    //base keywords we'll need to search and things we need to save for Hellowork
    xlsxFile('Populations.xlsx').then((rows) => {
        cats = rows[i][8];console.dir(rows[i][8]);
        })
        xlsxFile('Populations.xlsx').then((rows) => {
        places = rows[i][2];console.dir(rows[i][2]);
        })
        xlsxFile('Populations.xlsx').then((rows) => {
        if (y == 1) {
            metier = rows[i][3];
            console.dir(metier);
        }
        if(y == 2){
            metier = rows[i][4];
            console.dir(metier);
        }
        if(y == 3){
            metier = rows[i][5];
            console.dir(metier);
        }
        
        region = rows[i][1];
        console.dir(region);
        })
        /*
    if(region != 'Genève') {
        console.log("Ne cherche pas d'offre en Suisse !");
        return 0;
    } */
    //time to retrieve the urls and place them in a array of arrays
    // First the cookie check
    await page.goto(jobup, { waitUntil: 'domcontentloaded', timeout: 300000 });
    await page.setDefaultNavigationTimeout(0);
    console.log(`Navigating to ${jobup}...`);
    await utils.delay(3000);
    try { //
       // await page.waitForSelector("#modal-header");
        //let cookie = await page.$eval("button[data-cy='cookie-consent-modal-primary']", text => text.innerText);
        //await page.waitForSelector(cookie);
        //#modal > div > div > div > div > button > span
        await utils.delay(500);
        await page.focus("#modal > div > div > div > div > button > span");
        await page.click("#modal > div > div > div > div > button > span");
        await utils.delay(2000);
    } catch {
        console.log('failed cookies');
    }
    
    /* await page.keyboard.press('Tab');
    //await page.focus('#engine > div:nth-child(2) > div:nth-child(3) > input')
    await page.keyboard.type(region);
    await utils.delay(1000);
    await page.keyboard.press('ArrowDown');
    //await page.keyboard.press('ArrowDown'); #engine > div.whereinput > div:nth-child(3) > input
    await page.keyboard.press('Enter');
    await utils.delay(1000);
    //await page.keyboard.press('Enter');
    //await page.focus('#engine > div.cta_container > button');
    //await page.click('#engine > div.cta_container > button');
    */
    //we arrive to the page where the links are available
    await utils.delay(4000); ///html/body/main/section[1]/div/section/ul[1]/li[1]/div/div[2]/div[1]/span[2]/h3/a
    console.log("Link Page loaded");
    if(region=='Télétravail' ) {
        teleUrl = await page.url(); 
        teleUrl = teleUrl + "?benefit=1&term=";
        await page.goto(teleUrl, { waitUntil: 'domcontentloaded', timeout: 300000 });
        await page.setDefaultNavigationTimeout(0);
    } if(region=='Genève' && metier =='Assistant administratif') {
        await utils.delay(4000);
        teleUrl = await page.url(); 
        teleUrl = teleUrl + "?employment-type=5&employment-type=1&location=Genève&publication-date=1";
        await page.goto(teleUrl, { waitUntil: 'domcontentloaded', timeout: 300000 });
        await page.setDefaultNavigationTimeout(0);
    } else {
        await page.focus('#engine > div.whereinput > div:nth-child(3) > input');
        await page.click('#engine > div.whereinput > div:nth-child(3) > input');
        await page.keyboard.type(region);
        await utils.delay(1000);
        await page.keyboard.press('ArrowDown');
        await page.keyboard.press('Enter');
        await utils.delay(1000)
    }

    await page.focus('#synonym-typeahead-text-field');
    await page.click('#synonym-typeahead-text-field');
    await utils.delay(2000);
    //Then we search the site for our key terms
    await page.focus('#synonym-typeahead-text-field');
    await utils.delay(1000);
    await page.keyboard.type(metier);
    //await page.type('input[name=pickupAgingComment]', 'test comment', {delay: 20})
    await utils.delay(1000);
    await page.keyboard.press('ArrowDown');
    //await page.keyboard.press('ArrowDown');
    await page.keyboard.press('Enter');
    await page.keyboard.press('Enter');
    await utils.delay(1000);

    console.log("Link Page loaded");
    let hrefs = await page.$$eval('#skip-link-target > div> main > aside > div > div > div > div > div > article > a', as => as.map(a => a.href));
    // #skip-link-target > div> main > aside > div > div > div > div > div > article > a
        xlsxFile('Populations.xlsx').then((rows) => {
            cats = rows[i][8];
    })
    /* #skip-link-target > div > main > aside > div > div > div > div > div:nth-child(4) > article > a > div > div > span
    teleUrl = teleUrl.split("&p=1").join("&p=2")
        await page.goto(teleUrl, { waitUntil: 'domcontentloaded', timeout: 300000 });
        await page.setDefaultNavigationTimeout(0);
    let additionnalHrefs = await page.$$eval('html > body > main > section:nth-child(1) > div > section > ul:nth-child(1) > li > div > div:nth-child(2) > div:nth-child(1) > span:nth-child(2) > h3 >a', as => as.map(a => a.href));
    ///html/body/main/section[1]/div/section/ul[1]/li[6]/div/div[2]/div[1]/h3/a
        xlsxFile('Populations.xlsx').then((rows) => {
            cats = rows[i][8];
    })
    hrefs.push(additionnalHrefs).reduce((acc, curr) => acc.concat(curr),[]);
    */
    console.log("jobup has links : " + hrefs.length);
    if (region == "Télétravail"){

    } else if (hrefs.length >= 5){
        hrefs.length = 5;
    }
    return hrefs; 
},


async scrapeAnnoncePagejobupjob(page,i,y,ctr, url) { // Enables us to scrape the pages from the file
    let dataObj = {};
    await page.goto(url, {waitUntil: 'domcontentloaded', timeout: 300000});
    await page.setDefaultNavigationTimeout(0); // on dÃ©sactive le timeout de 30 secondes
    
    try { 
         await utils.delay(500);
         await page.focus("#modal > div > div > div > div > button > span");
         await page.click("#modal > div > div > div > div > button > span");
         await utils.delay(2000);
     } catch {
         console.log('failed cookies');
     }
    
    //'#skip-link-target > div > main > aside > div > div > div > div > div:nth-child(' + ctr + ') > article > a > div > div > span'
   /* await page.focus('h1');
    await page.click('h1'); */
    await utils.delay(3000);

    try {
        try {
        dataObj['date'] = await page.$eval('li[data-cy="info-publication"]', text => text.innerText);
        } catch {
            console.log("date failed");
        }
        dataObj['url'] = await page.url(); // stockage url de l'annonce
        dataObj['titre'] = await page.$eval('h1', text => text.textContent); // stockage du titre de l'annonce
        
        /*
        let activite = await page.$$eval('section[class="content retrait modal"] > ul > li', async catlinks => {
            // Extract the links from the data
            catlinks = await catlinks.map(el => el.textContent);
            return catlinks;
        });
        try {
        let metier = String(dataObj['titre']).split('        ')[2];
        dataObj['metier'] = metier;
        } catch {
            console.log("métier failed");
        }
        */
        /*
        try {
        let secteur = activite[2];
        dataObj['secteur'] = await doclean(secteur, true);
        } catch {
            console.log("secteur failed");
        }
        */
        try {
        let city = await page.$eval('a[data-cy="info-location-link"]', text => text.innerText);
        dataObj['ville'] = await doclean(city, true);
        } catch {
            console.log("ville failed");
        }
        /*
        try {
        let exp = activite[4];
        exp = exp.substr(33);
        dataObj['experience'] = await doclean(exp, false);
        } catch {
            console.log("experience failed"); //info-publication
        } */
        try { // await page.click('div[data-cy="info-contract"]'); await page.$eval('a[data-cy="cookie-consent-modal-primary"]', text => text.innerText);
        let contract = await page.$eval('div[data-cy="info-contract"]', text => text.innerText);
        contract = contract;//.substr(1);
        dataObj['contrat'] = await doclean(contract, false);
        } catch {
            console.log("contract failed");
        }
        /*
        let time = await page.$eval('.retrait > span', text => text.textContent) // stockage du titre de l'annonce
        const datePattern = /(\d{1,2})\/(\d{1,2})\/(\d{4})/;
        time = datePattern.exec(time);
        dataObj['postTime'] = time[0];
        */
        dataObj['description'] = await page.$eval('#skip-link-target > div > div > main > div > div > div > div > ul', text => text.innerText);

        console.log(dataObj);
        //console.log("DATAOBJ", dataObj);

        try {
                        
            dataObj['cats'] = cats;
            dataObj['places'] = places;

        } catch (error) {
            console.log("categories failed to save");
        }

        return (dataObj);
    }
    catch(err) {
        console.log(err);
        await page.close();
        return (0);
    }

}, 

async scrapeLinkPageApec(page, i, y) { //Gives us a table of pages in which we scrape
    let arr = [];
    let counter = 0;
    let table = [];
    let metier = '';
    let region = '';
    let teleUrl;
    await utils.delay(1000);
    xlsxFile('Populations.xlsx').then((rows) => {
    cats = rows[i][8];console.dir(rows[i][8]);
    })
    xlsxFile('Populations.xlsx').then((rows) => {
    places = rows[i][2];console.dir(rows[i][2]);
    })
    xlsxFile('Populations.xlsx').then((rows) => {
    if (y == 1) {
        metier = rows[i][3];
        console.dir(metier);
    }
    if(y == 2){
        metier = rows[i][4];
        console.dir(metier);
    }
    if(y == 3){
        metier = rows[i][5];
        console.dir(metier);
    }
    
    region = rows[i][1];
    console.dir(region);
    })
    
    await page.goto(apecUrl, { waitUntil: 'domcontentloaded', timeout: 300000 });
await page.setDefaultNavigationTimeout(0);
console.log(`Navigating to ${apecUrl}...`);
try {
    await utils.delay(2000);
    await page.click('button#onetrust-reject-all-handler');
    await utils.delay(1000);
} catch {
    console.log('failed cookies');
}

await page.focus('#keywords');
await page.click('#keywords');
await utils.delay(2000);
//Then we search the site for our key terms
await utils.delay(1000);
await page.keyboard.type(metier);
//await page.type('input[name=pickupAgingComment]', 'test comment', {delay: 20})
await utils.delay(1000);
await page.keyboard.press('Tab');

await utils.delay(1000);

if (region=='Télétravail'){
    console.log("Running TT APEC")
} else {
    await page.keyboard.type(region);
}
//await page.keyboard.press('ArrowDown');
//await page.keyboard.press('ArrowDown');
await utils.delay(1000);

await page.keyboard.press('Enter');
await utils.delay(1000);
//await page.keyboard.press('Tab');
await page.keyboard.press('Enter');

//we arrive to the page where the links are available
await utils.delay(2000); ///html/body/main/section[1]/div/section/ul[1]/li[1]/div/div[2]/div[1]/span[2]/h3/a
console.log("Link Page loaded");

if (region=='Télétravail'){
    await utils.delay(2000);
    teleUrl = await page.url(); 
    teleUrl = teleUrl + "&typesTeletravail=20766&typesTeletravail=20765&typesTeletravail=20767";
    await page.goto(teleUrl, { waitUntil: 'domcontentloaded', timeout: 300000 });
    await page.setDefaultNavigationTimeout(0);
}
await utils.delay(2000);
let hrefs = await page.$$eval('div.container-result > div > a', as => as.map(a => String(a.href)));

console.log(hrefs);
if(hrefs.length >= 5){
    hrefs.length = 5;
}
table.push(hrefs);
return table;

},

async scrapeAnnoncePageApec(page,i,y, url) { // Enables us to scrape the pages from the file
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
        dataObj['titre'] = await page.$eval('nav > div > div > h1', text => text.textContent); // stockage du titre de l'annonce
        let activite = await page.$$eval('.card-offer__text > .details-offer-list > li', async catlinks => { // on ne peux pas différencier les activiées par classe css donc on récupére la liste et on selectionne la case, on teste deux cases
            // Extract the links from the data
            catlinks = await catlinks.map(el => el.textContent);
            return catlinks;
        });
        
       // const activitesplit = String(activite[0]).split('\n');
     //   console.log("activite", activite);
     try {
                      
        dataObj['cats'] = cats;
        dataObj['places'] = places;

    } catch (error) {
        console.log("categories failed to save");
    }
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
/*
async scrapeAnnoncePageApec(page, url,i,y,) { // Enables us to scrape the pages from the file
    let dataObj = {};
    try {
        await page.goto(url, {waitUntil: 'domcontentloaded', timeout: 300000});
        console.log(`Navigating to ${apecUrl}...`);
        await page.setDefaultNavigationTimeout(0); // on désactive le timeout de 30 secondes
    }
    catch(err) {
        console.log(err);
        await page.goto(url, {waitUntil: 'domcontentloaded', timeout: 300000});
        await page.setDefaultNavigationTimeout(0); // on désactive le timeout de 30 secondes
    }
    
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
*/

async scrapeLinkPageRegionJob(page,i,y) { //Gives us a table of pages in which we scrape
    let arr = [];
    let counter = 1;
    let table = [];
    let choice = prompt("want to use Scrap France emploie ? yes or no \n");
    if(choice == "no"){
        return arr;
    }
    /*
    let i = prompt("number in population file \n");
    console.log('number = '+`${i}`);
    i--; //-1 because of title in "population"
    let y = prompt("choose job to scrape");
    console.log('job selected is n° '+`${y}`);
    */
    async function recall(){
    await page.setDefaultNavigationTimeout(0);
    await utils.delay(2000);
    if (counter===0){
    try {
        await page.waitForSelector('#didomi-popup > div > div > div > span');
        await utils.delay(2000);
    } catch {
        console.log('failed cookies');
    }
    }
    await utils.delay(2000);


    let hrefs = await page.$$eval('#listeAnn > ul > li > div.offer-info > div.libTypLoc > h2 > a', as => as.map(a => a.href));
    xlsxFile('Populations.xlsx').then((rows) => {
        cats = rows[i][8];
    })
   table = hrefs;
   console.log(table)
   
    } 
    while (counter <= 2) {
        console.log(counter);
        let keywordToHTML = "employé polyvalent";
        keywordToHTML = await keywordToHTML.replace(/ /g, '%20');
        xlsxFile('Populations.xlsx').then((rows) => {
            if (y == 1) {
                metier = rows[i][3];
                console.dir(rows[i][3]);
            }
            if(y == 2){
                metier = rows[i][4];
                console.dir(rows[i][4]);
            }
            if(y == 3){
                metier = rows[i][5];
                console.dir(rows[i][5]);
            }
            cats = rows[i][8];
            console.log(cats);
            region = rows[i][1];
            console.dir(rows[i][1]);
            finalstring = metier + "+" + region;
        })
        await utils.delay(2000);
        if (counter == 2){
            url = `${franceemploiURL}` + `${finalstring}` + "/2";
        }
        else{
            url = `${franceemploiURL}` + `${finalstring}`;
        }
        
        if (franceemploiURL.length < 10) {
            let arr = [];
            console.log('------------------------------------------------------------------------------------------------------------------- ');
            console.log(" LIEN FRANCE EMPLOI is Broken    -");
            console.log('------------------------------------------------------------------------------------------------------------------- ');
            return arr;
        } else {
            await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 300000 });
            await page.setDefaultNavigationTimeout(0);
            console.log(`Navigating to ${url}...`);
            await recall();
            await arr.push(table);
            table = [];
            ++counter;
        }
    }

        return arr; 
},

async scrapeAnnoncePageRegionJob(page, url) { // Enables us to scrape the pages from the file
     let dataObj = {};
        await page.goto(url, {waitUntil: 'domcontentloaded', timeout: 300000});
        await page.setDefaultNavigationTimeout(0); // on dÃ©sactive le timeout de 30 secondes
        
        
        try {
            dataObj['date'] = new Date().toISOString(); // date dans un format facile Ã  lire et reconvertir pour avoir un suivi
            dataObj['url'] = await page.url(); // stockage url de l'annonce


            temptitre = await page.$eval('#contenuFE > div > div.annonce-content > main > h2.libPoste.libelle-poste', text => text.textContent); // stockage du titre de l'annonce
            cleanstr = temptitre.replace(/(\r\n|\n|\r|\t)/gm, "");
            cleanstr = cleanstr.replace(/  +/g, ' '); 
            dataObj['titre'] = cleanstr;
            try {
                companytemp = await page.$eval('#lienLibelleEntreprise', text => text.textContent);
                cleanstr = companytemp.replace(/(\r\n|\n|\r|\t)/gm, "");
                cleanstr = cleanstr.replace(/  +/g, ' '); 
                dataObj['company'] = cleanstr; 
            } catch (error) {
                console.log("pas de company");
            }
            
            try {
                
                xlsxFile('Populations.xlsx').then((rows) => {
                dataObj['categories'] = rows[i][8];
                })

            } catch (error) {
                console.log("categories failed to save");
            }


            villetemp = await page.$eval('#contenuFE > div > div.annonce-content > main > dl > dd:nth-child(11)', text => text.textContent);
            cleanstr = villetemp.replace(/(\r\n|\n|\r|\t)/gm, "");
            cleanstr = cleanstr.replace(/  +/g, ' ');
            dataObj['ville'] = cleanstr; 

            desctemp = await page.$eval('#contenuFE > div > div.annonce-content > main > div:nth-child(7)', text => text.textContent);
            cleanstr = desctemp.replace(/(\r\n|\n|\r|\t)/gm, "");
            cleanstr = cleanstr.replace(/  +/g, ' '); 
            dataObj['description'] = cleanstr;
            
            let metier = String(dataObj['titre']).split('  ')[0];
            dataObj['metier'] = metier;

            try {
                experiencetemp = await page.$eval('#contenuFE > div > div.annonce-content > main > dl > dd:nth-child(17)', text => text.textContent);
                cleanstr = experiencetemp.replace(/(\r\n|\n|\r|\t)/gm, ""); 
                cleanstr = cleanstr.replace(/  +/g, ' '); 
                dataObj['experience'] = cleanstr;
            } catch (error) {
                console.log("pas d'experience")
            }


            try {
                dataObj['salary'] = await page.$eval('#contenuFE > div > div.annonce-content > main > dl > dd.salaire > span', text => text.textContent);
            } catch (error) {
                console.log("pas de salaire");
            }
            

           /* const xtime = "/html/body/section/article/div[5]/i/small/text()[2]"
            time = page.evaluate(xtime, page, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            time = time.innerHTML;
            time.split(' ');
            time = time[5];
            
            const datePattern = /(\d{1,2})\/(\d{1,2})\/(\d{4})/;
            time = datePattern.exec(time);*/
            temptime = await page.$eval('#contenuFE > div > div.annonce-content > main > dl > dd:nth-child(2) > span', text => text.textContent)
            dataObj['postTime'] = temptime;
            //console.log(dataObj)
            return (dataObj);
        }
        catch(err) {
            console.log(err);
            console.log(await page.url())
            await page.close();
            return (0);
        }

}, 

async scrapeLinkPagehellowork(page,i,y) { //Gives us a table of pages in which we scrape
    //base variables iterator and variables to store the data we'll need for Hellowork
    let arr = [];
    let counter = 1;
    let table = [];
    let metier = '';
    let region = '';
    let teleUrl;
    /*
    let choice = prompt("want to use Scrap Hello Work ? yes or no \n");
    if(choice == "no"||choice=='n'){
        return arr;
    }
    */
    //base keywords we'll need to search and things we need to save for Hellowork
    xlsxFile('Populations.xlsx').then((rows) => {
        cats = rows[i][8];console.dir(rows[i][8]);
       })
       xlsxFile('Populations.xlsx').then((rows) => {
        places = rows[i][2];console.dir(rows[i][2]);
       })
       xlsxFile('Populations.xlsx').then((rows) => {
        if (y == 1) {
            metier = rows[i][3];
            console.dir(metier);
        }
        if(y == 2){
            metier = rows[i][4];
            console.dir(metier);
        }
        if(y == 3){
            metier = rows[i][5];
            console.dir(metier);
        }
        
        region = rows[i][1];
        console.dir(region);
       })
     
    //time to retrieve the urls and place them in a array of arrays
    // First the cookie check
    await page.goto(helloworkURL, { waitUntil: 'domcontentloaded', timeout: 300000 });
    await page.setDefaultNavigationTimeout(0);
    console.log(`Navigating to ${helloworkURL}...`);
    try {
        await page.waitForSelector('#hw-cc-notice-continue-without-accepting-btn');
        await utils.delay(500);
        await page.focus('#hw-cc-notice-continue-without-accepting-btn');
        await page.click('#hw-cc-notice-continue-without-accepting-btn');
        await utils.delay(2000);
    } catch {
        console.log('failed cookies');
    }
    await page.focus('#engine > div > div:nth-child(3) > input');
    await page.click('#engine > div > div:nth-child(3) > input');
    await utils.delay(2000);
    //Then we search the site for our key terms
    await page.focus('#engine > div > div:nth-child(3) > input');
    await utils.delay(1000);
    await page.keyboard.type(metier);
    //await page.type('input[name=pickupAgingComment]', 'test comment', {delay: 20})
    await utils.delay(1000);
    await page.keyboard.press('ArrowDown');
    await page.keyboard.press('ArrowDown');
    await page.keyboard.press('Enter');
    await page.keyboard.press('Enter');
    await utils.delay(1000);
    /* await page.keyboard.press('Tab');
    //await page.focus('#engine > div:nth-child(2) > div:nth-child(3) > input')
    await page.keyboard.type(region);
    await utils.delay(1000);
    await page.keyboard.press('ArrowDown');
    //await page.keyboard.press('ArrowDown'); #engine > div.whereinput > div:nth-child(3) > input
    await page.keyboard.press('Enter');
    await utils.delay(1000);
    //await page.keyboard.press('Enter');
    //await page.focus('#engine > div.cta_container > button');
    //await page.click('#engine > div.cta_container > button');
    */
    //we arrive to the page where the links are available
    await utils.delay(4000); ///html/body/main/section[1]/div/section/ul[1]/li[1]/div/div[2]/div[1]/span[2]/h3/a
    console.log("Link Page loaded");
    if(region=='Télétravail') {
        teleUrl = await page.url(); 
        teleUrl = teleUrl + "&t=Complet&t=Partiel&t=Occasionnel" + "&c=CDI&c=CDD";
        await page.goto(teleUrl, { waitUntil: 'domcontentloaded', timeout: 300000 });
        await page.setDefaultNavigationTimeout(0);
        /*
        try {
            await page.waitForSelector('.serp');
            try {
                const btnval = await document.querySelector("body > main > section > div > div.md\\:tw-pt-2.md\\:tw-bg-white.md\\:tw-rounded-2xl.md\\:tw-shadow-card.side > div.side > div:nth-child(7) > div");//select(page).getElement(`section > div > div > div:nth-child(7) > div > label > div`);
                let ttButton0 = btnval;
                await utils.delay(1000);
                await page.focus(ttButton0);
                await page.click(ttButton0);
                await utils.delay(1000);
            } catch {
                console.log('tt 1 failed');
            }
            
            try {
                let ttcButton = await select(page).getElement(`li:contains(Complet)`);
                await utils.delay(1000);
                await page.focus(ttcButton);
                await page.click(ttcButton);
                await utils.delay(1000); 
            } catch {
                console.log('tt 2 failed');
            }
            
            try {
                let ttpButton = await select(page).getElement(`li:contains(Partiel)`);
                await utils.delay(1000);
                await page.focus(ttpButton);
                await page.click(ttpButton);
                await utils.delay(1000);
            }  catch {
                console.log('tt3 failed');
            }
            
        } catch {
            console.log('tt failed');
        }
        */
    } else {
        await page.focus('#engine > div.whereinput > div:nth-child(3) > input');
        await page.click('#engine > div.whereinput > div:nth-child(3) > input');
        await page.keyboard.type(region);
        await utils.delay(1000);
        await page.keyboard.press('ArrowDown');
        await page.keyboard.press('Enter');
        await utils.delay(4000)
    }
    
    let hrefs = await page.$$eval('html > body > main > section:nth-child(1) > div > section > ul:nth-child(1) > li > div > div:nth-child(2) > div:nth-child(1) > span:nth-child(2) > h3 >a', as => as.map(a => a.href));
    ///html/body/main/section[1]/div/section/ul[1]/li[6]/div/div[2]/div[1]/h3/a
        xlsxFile('Populations.xlsx').then((rows) => {
            cats = rows[i][8];
    })
    /*
    teleUrl = teleUrl.split("&p=1").join("&p=2")
        await page.goto(teleUrl, { waitUntil: 'domcontentloaded', timeout: 300000 });
        await page.setDefaultNavigationTimeout(0);
    let additionnalHrefs = await page.$$eval('html > body > main > section:nth-child(1) > div > section > ul:nth-child(1) > li > div > div:nth-child(2) > div:nth-child(1) > span:nth-child(2) > h3 >a', as => as.map(a => a.href));
    ///html/body/main/section[1]/div/section/ul[1]/li[6]/div/div[2]/div[1]/h3/a
        xlsxFile('Populations.xlsx').then((rows) => {
            cats = rows[i][8];
    })
    hrefs.push(additionnalHrefs).reduce((acc, curr) => acc.concat(curr),[]);
    */
    console.log("hellowork length is: " + hrefs.length);
    if (region == "Télétravail"){

    }else if (hrefs.length >= 5){
        hrefs.length = 5;
    }
    return hrefs; 
},


async scrapeAnnoncePageHelloWork(page,i,y, url) { // Enables us to scrape the pages from the file
    let dataObj = {};
    await page.goto(url, {waitUntil: 'domcontentloaded', timeout: 300000});
    await page.setDefaultNavigationTimeout(0); // on dÃ©sactive le timeout de 30 secondes
    
    try {
        await page.waitForSelector('button#hw-cc-notice-accept-btn');
        await utils.delay(2000);
        await page.click('button#hw-cc-notice-accept-btn');
        await utils.delay(1000);
    } catch {
        console.log('failed cookies');
    }
    
    try {
        dataObj['date'] = new Date().toISOString(); // date dans un format facile Ã  lire et reconvertir pour avoir un suivi
        dataObj['url'] = await page.url(); // stockage url de l'annonce
        dataObj['titre'] = await page.$eval('h1 > span', text => text.textContent); // stockage du titre de l'annonce
        let activite = await page.$$eval('section[class="content retrait modal"] > ul > li', async catlinks => {
            // Extract the links from the data
            catlinks = await catlinks.map(el => el.textContent);
            return catlinks;
        });
        try {
        let metier = String(dataObj['titre']).split('        ')[2];
        dataObj['metier'] = metier;
        } catch {
            console.log("métier failed");
        }
        try {
        let secteur = activite[2];
        dataObj['secteur'] = await doclean(secteur, true);
        } catch {
            console.log("secteur failed");
        }
        try {
        let city = activite[0];
        dataObj['ville'] = await doclean(city, true);
        } catch {
            console.log("ville failed");
        }
        try {
        let exp = activite[4];
        exp = exp.substr(33);
        dataObj['experience'] = await doclean(exp, false);
        } catch {
            console.log("experience failed");
        }
        try {
        let contract = activite[1];
        contract = contract;//.substr(1);
        dataObj['contrat'] = await doclean(contract, false);
        } catch {
            console.log("contract failed");
        }
        try {
        let salary = activite[6];
        dataObj['salary'] = await doclean(salary, true);
        } catch {
            console.log("salary failed");
        }
        let time = await page.$eval('.retrait > span', text => text.textContent) // stockage du titre de l'annonce
        const datePattern = /(\d{1,2})\/(\d{1,2})\/(\d{4})/;
        time = datePattern.exec(time);
        dataObj['postTime'] = time[0];

        dataObj['description'] = await page.$eval('section[class="content modal"]', text => text.innerText);

        console.log(activite);
        //console.log("DATAOBJ", dataObj);

        try {
                      
            dataObj['cats'] = cats;
            dataObj['places'] = places;

        } catch (error) {
            console.log("categories failed to save");
        }

        return (dataObj);
    }
    catch(err) {
        console.log(err);
        await page.close();
        return (0);
    }

}, 

async scrapeCurrentPagePe(page,i,y) { //Gives us a table of pages in which we scrape
   let counter = 1;
   /*
   let choice = prompt("want to use Scrap Pole emploie ? yes or no \n");
   if(choice == "no"){
      // urlcat = "";
       return //urlcat;
   }
   */
   /*
   let i = prompt("number in population file \n");
   console.log('number = '+`${i}`);
   i--; //-1 because of title in "population"
   let y = prompt("choose job to scrape ");
   console.log('job selected is n° '+`${y}`);
   */
   xlsxFile('Populations.xlsx').then((rows) => {
    cats = rows[i][8];console.dir(rows[i][8]);
   })
   xlsxFile('Populations.xlsx').then((rows) => {
    places = rows[i][2];console.dir(rows[i][2]);
   })
   xlsxFile('Populations.xlsx').then((rows) => {
    if (y == 1) {
        metier = rows[i][3];
        console.dir(rows[i][3]);
    }
    if(y == 2){
        metier = rows[i][4];
        console.dir(rows[i][4]);
    }
    if(y == 3){
        metier = rows[i][5];
        console.dir(rows[i][5]);
    }
    
    region = rows[i][1];
    console.dir(rows[i][1]);
   })
    urlPe = `https://candidat.pole-emploi.fr/offres/emploi`;
    await page.goto(urlPe, {waitUntil: 'domcontentloaded', timeout: 300000});
            await page.setDefaultNavigationTimeout(0);
            console.log(`Navigating to ${urlPe}...`);

    try {
        await page.waitForSelector('a.footer_tc_privacy_content');
        await utils.delay(2000);
        await page.click('a.footer_tc_privacy_content');
        await utils.delay(1000);
    } catch {
        console.log('failed cookie button');
    } 
    await page.focus('#idmotsCles-selectized')
    if (region == 'Télétravail') {
        await page.keyboard.type(metier);
        await page.keyboard.press('Enter');
        await page.keyboard.press('Tab');
        await page.keyboard.type(region);
        await page.keyboard.press('Enter');
        await page.keyboard.press('Tab');
    } else {
        await page.keyboard.type(metier)
    }
    await page.keyboard.press('Enter');
    await page.focus('#idlieux-selectized')
    if (region == 'Télétravail') {
        console.log('Running TT PE')
    } else {
        await page.keyboard.type(region.split(' - ')[0])
    }
    await utils.delay(1000);
    await page.keyboard.press('Enter');
    await page.click('#btnSubmitRechercheForm')
    console.log(page.url())
    /*
    await utils.delay(3000);
    await page.click('#filter-date-creation')
    await page.click('#newfilters > ul > li.btn-group.dropdown.open > div > fieldset > ul > li:nth-child(2) > label')
    await utils.delay(1000);
    await page.click('#newfilters > ul > li.btn-group.dropdown.open > div > div > a')*/
    await utils.delay(1000);
    while(counter<=6){
    ++counter;
        try {
            await utils.delay(2000);
            await page.click('.results-more > a');
            await utils.delay(1000);
        } catch {
            console.log('failed next button breaking');
            break;

        } 
    }
    let urlcat = await page.$$eval('li.result', catlink => {
        // Extract the links from the data
        catlink = catlink.map(el => el.querySelector('a.with-fav').href);
        return catlink;
      });
    if (urlcat.length >= 10) {
      urlcat.length = 10;
    }    
    console.log(urlcat);
        return urlcat; 
},


async scrapeAnnoncePagePe(page,i,y, url) { // Enables us to scrape the pages from the file
    let dataObj = {};
    await page.goto(url, {waitUntil: 'domcontentloaded', timeout: 300000});
    await page.setDefaultNavigationTimeout(0); // on dÃ©sactive le timeout de 30 secondes
    
    try {
        await page.waitForSelector('a.footer_tc_privacy_content');
        await utils.delay(2000);
        await page.click('a.footer_tc_privacy_content');
        await utils.delay(1000);
    } catch {
        console.log('failed cookie button');
    } 
    await page.waitForSelector('.modal-body');
    try {
        dataObj['date'] = new Date().toISOString(); // date dans un format facile Ã  lire et reconvertir pour avoir un suivi
        dataObj['url'] = await page.url(); // stockage url de l'annonce
        dataObj['titre'] = await page.$eval('h1', text => text.textContent); // stockage du titre de l'annonce
       try {
        dataObj['salaire'] = await page.$eval('div.description-aside.col-sm-4.col-md-5 > dl > dd:nth-child(7) > ul > li', text => text.textContent);
       } catch(err) {
        console.log("Salary Fail");
    }   
        try {
            dataObj['contrat'] = await page.$eval('div.description-aside.col-sm-4.col-md-5 > dl > dd:nth-child(5)', text => text.textContent);
        } catch(err) {
            console.log("Contract Fail");
        } 
        
        dataObj['experience'] = await page.$eval('li > span > span.skill-name', text => text.textContent);
        dataObj['ville'] = await page.$eval('p.t4.title-complementary > span:nth-child(1)', text => text.textContent);
        dataObj['postTime'] = await page.$eval('p.t5.title-complementary > span:nth-child(1)', text => text.textContent);
        const datePattern = /(\d{1,2})\/(\d{1,2})\/(\d{4})/;

        try {
                      
            dataObj['cats'] = cats;
            dataObj['places'] = places;

        } catch (error) {
            console.log("categories failed to save");
        }

        dataObj['description'] = await page.$eval('div > div > div > div > div > div > div > div > div > div > div.description > p', text => text.textContent);

        console.log(dataObj);

        return (dataObj);
    }
    catch(err) {
        console.log(err);
        await page.close();
        return (0);
    }
}, 

async scrapeLinktpjb(page,i,y) { //Gives us a table of pages in which we scrape
    //base variables iterator and variables to store the data we'll need for Hellowork
    let arr = [];
    let counter = 1;
    let table = [];
    let metier = '';
    let region = '';
    let choice = prompt("want to use teepy-job.com scrap ? yes or no \n");
    if(choice == "no"||choice=='n'){
        return arr;
    }
    metier = prompt("What Cat do you wish to scrap in teepy-job.com\n");
    
    region = prompt("What Location do you wish to scrap in teepy-job.com\n");

    console.log("Vous rechercher un "+metier+' vers '+region+'.');
    let confirmation = prompt("confirm scrape");
    if(confirmation == "no"||confirmation=='n'){
        choice = prompt("Cancel scrap ? ? yes or no \n");
        if(choice == "yes"||choice=='y'){
            return arr;
        }
    } else {
        metier = prompt("What Cat do you wish to scrap in teepy-job.com\n");
    
        region = prompt("What Location do you wish to scrap in teepy-job.com\n");
    }
    //base keywords we'll need to search and things we need to save for Hellowork
    /*
    xlsxFile('Populations.xlsx').then((rows) => {
        cats = rows[i][8];console.dir(rows[i][8]);
       })
       xlsxFile('Populations.xlsx').then((rows) => {
        places = rows[i][2];console.dir(rows[i][2]);
       })
       xlsxFile('Populations.xlsx').then((rows) => {
        if (y == 1) {
            metier = rows[i][3];
            console.dir(metier);
        }
        if(y == 2){
            metier = rows[i][4];
            console.dir(metier);
        }
        if(y == 3){
            metier = rows[i][5];
            console.dir(metier);
        }
        
        region = rows[i][1];
        console.dir(region);
       })
     */

    //time to retrieve the urls and place them in a array of arrays
    // First the cookie check
    await page.goto(teepyjobURL, { waitUntil: 'domcontentloaded', timeout: 300000 });
    await page.setDefaultNavigationTimeout(0);
    console.log(`Navigating to ${teepyjobURL}...`);
    try {
        await page.waitForSelector('#cookieChoiceDismiss');
        await utils.delay(500);
        await page.focus('#cookieChoiceDismiss');
        await page.click('#cookieChoiceDismiss');
        await utils.delay(2000);
    } catch {
        console.log('failed cookies');
    }
    //Then we search the site for our key terms
    await page.focus('#metier-rech');
    await page.keyboard.type(metier);
    await page.keyboard.press('Tab');
    await page.focus('#loc-rech')
    await page.keyboard.type(region);
    await utils.delay(1000);
    //await page.keyboard.press('Enter');
    await page.focus('#go-rech');
    await page.click('#go-rech');
    //we arrive to the page where the links are available
    await utils.delay(1000);
    console.log(page.url())
    await utils.delay(1000);
    /*
    while(counter<=2) {
        try {
            await page.waitForSelector('#contenu > div.row.contcont > div.col-xs-12.col-sm-12.col-md-4.col-lg-4 > button');
            await page.focus('#contenu > div.row.contcont > div.col-xs-12.col-sm-12.col-md-4.col-lg-4 > button');
            await page.click('#contenu > div.row.contcont > div.col-xs-12.col-sm-12.col-md-4.col-lg-4 > button');
            await utils.delay(2000);
        } catch(err) {
            console.log('All the page links have been found.');
            await utils.delay(1000);
            counter = 2;
            break;
        }
    }
    */
    let loopVar= 1;
    while(counter <=3) {
        try {
            await utils.delay(1000);
            await page.waitForSelector('html > body > divnth-child(3) > divnth-child(4) > divnth-child(2) > divnth-child(2) > div['+loopVar+']');
            await page.focus('html > body > divnth-child(3) > divnth-child(4) > divnth-child(2) > divnth-child(2) > div['+loopVar+']');
            await page.click('html > body > divnth-child(3) > divnth-child(4) > divnth-child(2) > divnth-child(2) > div['+loopVar+']');
            await utils.delay(1000);
            let hrefs = await page.$$eval('#zone-det > div > div.ann-scroll > div:nth-child(3) > a', as => as.map(a => a.href));
            await utils.delay(1000);
            table = hrefs;
            console.log(table);
            arr.push(table);
            table = [];
        } catch(err) {
            await utils.delay(1000);
            console.log('All links have been found');
            counter = 3;
            break;
        }
    }
    return arr;
    ///html/body/divnth-child(3)/divnth-child(4)/divnth-child(2)/divnth-child(2)/div[22]
    ///html/body/div[3]/div[4]/div[2]/div[2]/div[1]
    //#zone-det > div > div.ann-scroll > div:nth-child(3) > a
    /*
    while (counter <= 2) {
        console.log(page.url())
        try {
            
            await page.waitForSelector('#cookieChoiceDismiss');
            await utils.delay(500);
            await page.click('#cookieChoiceDismiss');
            await utils.delay(1000);
        } catch {
            console.log('failed cookies');
        }
        let hrefs = await page.$$eval('html > body > main > section:nth-child(1) > div > section > ul:nth-child(1) > li > div > div:nth-child(2) > div:nth-child(1) > h3 >a', as => as.map(a => a.href));
        ///html/body/main/section[1]/div/section/ul[1]/li[6]/div/div[2]/div[1]/h3/a
            xlsxFile('Populations.xlsx').then((rows) => {
                cats = rows[i][8];
            })
        if(hrefs.length>0) {
        table = hrefs;
        console.log(table);
        arr.push(table);
        table = [];
        }
        counter++;
        await page.focus('#pagin > div > div > div:nth-child(2) > div > ul > li.next');
        await page.click('#pagin > div > div > div:nth-child(2) > div > ul > li.next');
        await utils.delay(1000);
    }
    return arr;
    */ 
},


async scrapeAnnoncePageAnnonctpjob(page,i,y, url) { // Enables us to scrape the pages from the file
    let dataObj = {};
    await page.goto(url, {waitUntil: 'domcontentloaded', timeout: 300000});
    await page.setDefaultNavigationTimeout(0); // on dÃ©sactive le timeout de 30 secondes
    
    try {
        await page.waitForSelector('button#hw-cc-notice-accept-btn');
        await utils.delay(2000);
        await page.click('button#hw-cc-notice-accept-btn');
        await utils.delay(1000);
    } catch {
        console.log('failed cookies');
    }
    
    try {
        dataObj['date'] = new Date().toISOString(); // date dans un format facile Ã  lire et reconvertir pour avoir un suivi
        dataObj['url'] = await page.url(); // stockage url de l'annonce
        dataObj['titre'] = await page.$eval('h1 > span', text => text.textContent); // stockage du titre de l'annonce
        let activite = await page.$$eval('section[class="content retrait modal"] > ul > li', async catlinks => {
            // Extract the links from the data
            catlinks = await catlinks.map(el => el.textContent);
            return catlinks;
        });
        let metier = String(dataObj['titre']).split('        ')[2];
        dataObj['metier'] = metier;
        let secteur = activite[2];
        dataObj['secteur'] = await doclean(secteur, true);
        let city = activite[0];
        dataObj['ville'] = await doclean(city, true);
        let exp = activite[4];
        exp = exp.substr(33);
        dataObj['experience'] = await doclean(exp, false);
        let contract = activite[1];
        contract = contract;//.substr(1);
        dataObj['contrat'] = await doclean(contract, false);
        let salary = activite[6];
        dataObj['salary'] = await doclean(salary, true);
        
        let time = await page.$eval('.retrait > span', text => text.textContent) // stockage du titre de l'annonce
        const datePattern = /(\d{1,2})\/(\d{1,2})\/(\d{4})/;
        time = datePattern.exec(time);
        dataObj['postTime'] = time[0];

        dataObj['description'] = await page.$eval('section[class="content modal"]', text => text.innerText);

        console.log(activite);
        //console.log("DATAOBJ", dataObj);

        try {
                      
            dataObj['cats'] = cats;
            dataObj['places'] = places;

        } catch (error) {
            console.log("categories failed to save");
        }

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