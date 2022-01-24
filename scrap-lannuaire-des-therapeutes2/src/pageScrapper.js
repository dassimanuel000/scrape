const fs = require('fs');
async function delay(time) {
    return new Promise(function(resolve) { 
        setTimeout(resolve, time)
    });
 }
 async function jsonExport(scrapedCatData) {
     // put json object in a file
     var jsonContent = await JSON.stringify(scrapedCatData);
    await fs.writeFile("./output.json", jsonContent, 'utf8', function (err) { //03/11/21 + l'annuaire des thérapeutes
        if (err) {
            console.log("An error occured while writing JSON Object to File.");
            return console.log(err);
        }
        console.log("JSON file has been saved.");
    });
 }
const scraperObject = {
    url: 'https://annuairetherapeutes.fr/lannuaire-des-therapeutes/page/38/?address%5B0%5D=France&post%5B0%5D=post&tax%5Bpost_tag%5D%5B0%5D&distance=200&units=metric&per_page=48&lat=46.227638&lng=2.213749&form=1&action=fs&country=FR',
    async scraper(browser) {
        let page = await browser.newPage();
        console.log(`Navigating to ${this.url}...`);
        await page.setDefaultNavigationTimeout(0); 
        await page.goto(this.url);
        // Wait for the required DOM to be rendered
        let scrapedCatData = [];
        let scrapeCurrentPageCount = 0;

        async function scrapeCurrentPage(){
            scrapeCurrentPageCount++;

        console.log(scrapeCurrentPageCount);
        page.waitForNavigation({ waitUntil: 'networkidle2' });
        await page.waitForSelector('.gmw-results-wrapper-1');
        
        let urls = await page.$$eval('.posts-list-wrapper > li > div > div > div.post-thumbnail', catlink => {
            // Extract the links from the data
            catlink = catlink.map(el => el.querySelector('a').href);
            return catlink;
          });
        console.log("testing url : ", urls);
        let pagePromise = (urls) => new Promise(async(resolve, reject) => {
            let dataObj = {};
            let profPage = await browser.newPage();
            await profPage.setDefaultNavigationTimeout(0); 
            await profPage.goto(urls);
            try {
            await profPage.waitForSelector('div.vcard');
            page.waitForNavigation({ waitUntil: 'networkidle2' });
            try {
            //console.log("0");
            dataObj['nom'] = await profPage.$eval('div.vcard > div.csc > div.tth > h1', text => text.textContent);
            //dataObj['titre'] = await profPage.$eval('.title > h1', text => text.textContent);
            //console.log("1");
            dataObj['description'] = await profPage.$eval('.org', text => text.textContent);
            //console.log("2");
            dataObj['addresse'] = await profPage.$eval('div.vcard > div > div > div > div.adr', text => text.textContent);
            //console.log("3");
            dataObj['telephone'] = await profPage.$eval('div.vcard > div > div > div#borduredroitecoordonnees > p ', text => text.textContent); // need click then take it
            
            //let datetmp= await profPage.$eval('.published', text => text.textContent); // need click then take it
            //dataObj['date'] = datetmp.substr(12);
            //let date = dataObj['date'];
            //let dateTest = new Date(date);
            //console.log(dateTest);
            console.log(dataObj);
            resolve(dataObj);
            }
            catch {
                console.log("Missing info for full profile");
                resolve(dataObj);
                console.log("Post resolve");
            }
        }
        catch {
            console.log("Page error");
                resolve(dataObj);
                console.log("Page pass");
        }
            //console.log('resolve succeeded');
            await profPage.close();
        });

        let counter = 0;
        while (urls[counter]) {
            let currentPageData = await pagePromise(urls[counter]);
            //console.log("counter");
            try {
            scrapedCatData.push(currentPageData);
            } 
            catch {
                console.log("Error Finding data");
            }
            //console.log(counter);
            ++counter;
            console.log(urls.length);
            if(urls.length == counter+1){
                let nextButtonExist = false;
                    try{
                        const nextButton = await page.$eval('.next', a => a.textContent);
                        nextButtonExist = true;
                    }
                    catch(err){
                        nextButtonExist = false;
                    }
                    if(nextButtonExist){
                        await page.click('.next');
                        counter = 0;
                        return await scrapeCurrentPage(); // Call this function recursively
                    }
            }
        }
            await page.close();
            return scrapedCatData;
    }
    let data = await scrapeCurrentPage(); 
    //resolve(data);
    // build next
    console.log("done");
    await jsonExport(scrapedCatData);
    return data;
    }
}

module.exports = scraperObject;