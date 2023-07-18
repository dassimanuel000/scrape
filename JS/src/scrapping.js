const utils = require('./utils');
const xlsxFile = require('read-excel-file/node');
const prompt = require('prompt-sync')();
let counter = 0;
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
async scrapeLinkPageApec(page,region,metier) { //Gives us a table of pages in which we scrape

    let table = [];
    await page.goto(apecUrl, { waitUntil: 'domcontentloaded', timeout: 300000 });
    await page.setDefaultNavigationTimeout(0);
    console.log(`Navigating to ${apecUrl}...`);
    try {
        await utils.delay(2000);
        await page.click('div#onetrust-button-group > button#onetrust-accept-btn-handler');
        await utils.delay(1000);
    } catch {
        console.log('failed cookies');
    }

    await page.focus('html > body > main > div > section > div > div > div > form > div > div >div:nth-child(1) > input');
    await page.click('html > body > main > div > section > div > div > div > form > div > div >div:nth-child(1) > input');
    await utils.delay(2000);
    //Then we search the site for our key terms
    await utils.delay(1000);
    await page.keyboard.type(metier);
    //await page.type('input[name=pickupAgingComment]', 'test comment', {delay: 20})
    await utils.delay(1000);
    await page.keyboard.press('Tab');

    await utils.delay(1000);
    await page.keyboard.type(region);
    await utils.delay(1000);

    await page.keyboard.press('Enter');
    await utils.delay(1000);
    await page.keyboard.press('Tab');
    await page.keyboard.press('Enter');

    //we arrive to the page where the links are available
    await utils.delay(3000); ///html/body/main/section[1]/div/section/ul[1]/li[1]/div/div[2]/div[1]/span[2]/h3/a
    console.log("Link Page loaded");
    let hrefs = await page.$$eval('.container-result > div > a', as => as.map(a => String(a.href)));

    console.log(hrefs);
    if(hrefs.length >= 5){
        hrefs.length = 5;
    }
    table.push(hrefs);
    return table;

},

async scrapeAnnoncePageApec(page, url,cats, place) { // Enables us to scrape the pages from the file
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
     try {
                      
        dataObj['lieux'] = place;
        dataObj['categorie'] = cats;

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

async scrapeLinkPageRegionJob(page,region,metier) { //Gives us a table of pages in which we scrape
    let arr = [];
    let counter = 1;
    let table = [];

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
    if(hrefs.length >= 5){
        hrefs.length = 5;
    }
    table = hrefs;
    console.log(table)
   
    } 
        finalstring = metier + "+" + region;
        url = `${franceemploiURL}` + `${finalstring}`;

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

        return arr; 
},

async scrapeAnnoncePageRegionJob(page, url, cats, place,) { // Enables us to scrape the pages from the file
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
                companytemp = await page.$eval('#contenuFE > div > div.annonce-content > main > dl > dd:nth-child(5)', text => text.textContent);
                cleanstr = companytemp.replace(/(\r\n|\n|\r|\t)/gm, "");
                cleanstr = cleanstr.replace(/  +/g, ' '); 
                dataObj['compagny'] = cleanstr; 
            } catch (error) {
                console.log("pas de company");
            }
            
            try {
                dataObj['lieux'] = place;
                dataObj['categorie'] = cats;
                
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

async scrapeLinkPagehellowork(page,region,metier) { //Gives us a table of pages in which we scrape     
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
    await page.focus('#engine > div.cta_container > button');
    await page.click('#engine > div.cta_container > button');
    await utils.delay(2000);
    //Then we search the site for our key terms
    await page.focus('#engine > div.whatinput > div:nth-child(3) > input');
    await utils.delay(1000);
    await page.keyboard.type(metier);
    //await page.type('input[name=pickupAgingComment]', 'test comment', {delay: 20})
    await utils.delay(1000);
    await page.keyboard.press('ArrowDown');
    await page.keyboard.press('ArrowDown');
    await page.keyboard.press('Enter');
    //await page.keyboard.press('Tab');
    await page.focus('#engine > div.whereinput > div:nth-child(3) > input')
    await page.keyboard.type(region);
    await utils.delay(1000);
    await page.keyboard.press('ArrowDown');
    //await page.keyboard.press('ArrowDown');
    await page.keyboard.press('Enter');
    await utils.delay(1000);
    //await page.keyboard.press('Enter');
    await page.focus('#engine > div.cta_container > button');
    await page.click('#engine > div.cta_container > button');
    
    //we arrive to the page where the links are available
    await utils.delay(3000); ///html/body/main/section[1]/div/section/ul[1]/li[1]/div/div[2]/div[1]/span[2]/h3/a
    console.log("Link Page loaded");
    let hrefs = await page.$$eval('html > body > main > section:nth-child(1) > div > section > ul:nth-child(1) > li > div > div:nth-child(2) > div:nth-child(1) > span:nth-child(2) > h3 >a', as => as.map(a => a.href));
    ///html/body/main/section[1]/div/section/ul[1]/li[6]/div/div[2]/div[1]/h3/a
    console.log(hrefs);
    if(hrefs.length >= 5){
        hrefs.length = 5;
    }
    return hrefs; 
},


async scrapeAnnoncePageHelloWork(page, url, cats, place) { // Enables us to scrape the pages from the file
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
            dataObj['lieux'] = place;
            dataObj['categorie'] = cats;

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

async scrapeCurrentPagePe(page,region,metier) { //Gives us a table of pages in which we scrape
   let counter = 1;
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
    await page.keyboard.type(metier)
    await page.keyboard.press('Enter');
    await page.focus('#idlieux-selectized')
    await page.keyboard.type(region)
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


async scrapeAnnoncePagePe(page,url, cats, place) { // Enables us to scrape the pages from the file
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
        dataObj['titre'] = await page.$eval('h1>span:nth-child(3)', text => text.textContent); // stockage du titre de l'annonce
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
	dataObj['compagny'] = await page.$eval('div.media-body>h3.t4.title', text => text.textContent);
        dataObj['skills'] = await page.evaluate(() => {
            const skillList = Array.from(document.querySelectorAll('ul.skill-list.list-unstyled li .skill-name'));
            return skillList.map(skill => skill.textContent).join(' <br> ');
          });
        const datePattern = /(\d{1,2})\/(\d{1,2})\/(\d{4})/;

        try {
                      
            dataObj['lieux'] = place;
            dataObj['categorie'] = cats;

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
};

module.exports = scrapping;