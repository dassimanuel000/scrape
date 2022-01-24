const psycho = require('./todaypsycholog');
const mongoose = require('mongoose');

async function delay(time) {
    return new Promise(function(resolve) { 
        setTimeout(resolve, time)
    });
 }

let profData = [];

const scraperObject = {
    url: 'https://annuairetherapeutes.fr/lannuaire-des-therapeutes/?address%5B0%5D=France&post%5B0%5D=post&tax%5Bpost_tag%5D%5B0%5D&distance=200&units=metric&per_page=48&lat=46.227638&lng=2.213749&form=1&action=fs&country=FR',
    async scraperCat(page) {
        //let page = await browser.newPage();
        console.log(`Navigating to ${this.url}...`);
        await page.goto(this.url, {waitUntil: 'domcontentloaded', timeout: 300000});
        //await page.goto(this.url);
        async function scrapeCurrentPage(){
        await page.setDefaultNavigationTimeout(0);
        // Wait for the required DOM to be rendered
        await page.waitForSelector('.posts-list-wrapper');
        // Get the link to all the required books
        let urls = await page.$$eval('.posts-list-wrapper > li > div > div > div.post-thumbnail', links => {
            // Extract the links from the data
            links = links.map(el => el.querySelector('a').href);
            return links;
        });
        console.log("urls", urls);
        return urls;
    }
        let urls = await scrapeCurrentPage(); 
        console.log("done getcat");
        return urls;
    },

    async scraper(page, urlCategory) {
            //let page = await browser.newPage();
            console.log(`Navigating to ${urlCategory.url}...`);
            await page.goto(urlCategory.url, {waitUntil: 'domcontentloaded', timeout: 300000});
        async function scrapeCurrentPages(){
            await page.setDefaultNavigationTimeout(0);
            // Wait for the required DOM to be rendered
            await page.waitForSelector('.vcard');
            // Get the link to all the required books
            let urlcat = await page.$$eval('div.vcard > div.csc > div.colm > h1', catlinks => {
            // Extract the links from the data
            catlinks = catlinks.map(el => el.href);
            return catlinks;
            });
            
            console.log("profile url", urlcat);
            let getProfileData = (urls) => new Promise(async(resolve, reject) => {
                let dataObj = {};
                //let profPage = await browser.newPage();
                console.log("Profile", urls);
                await page.goto(urls, {waitUntil: 'domcontentloaded', timeout: 300000});
                try {
                    await page.waitForSelector('.profile-name-phone');
                    dataObj['nom'] = await page.$eval('div.vcard > div.csc > div.colm > h1', text => text.textContent);
                    dataObj['activite'] = await page.$eval('.profile-name-phone > div > div > h2 > span > button > span', text => text.textContent);
                    dataObj['addresse'] = await page.$eval('.location-address-phone > span[itemprop="addressLocality"]', text => text.textContent);
                    try {
                        dataObj['telephone'] = await page.$eval('#phone-click-reveal', text => text.href);
                        dataObj['telephone'] = dataObj['telephone'].substring(4);
                        //resolve(dataObj);
                        //await page.close();
                    } catch (err) {
                        dataObj['telephone'] = "";
                        //resolve(dataObj);
                        //await page.close();
                        console.log("error", err);
                    }
                } catch (err) {console.log("here an error", err);}
                resolve(dataObj);
                console.log(dataObj);
                return dataObj;
            });

            for (let counter = 0; counter < urlcat.length; counter++) {
                    let dataObj = await getProfileData(urlcat[counter]);

                    await mongoose.connect('mongodb://localhost/annuairetherapeutes', {
                    useNewUrlParser: true,
                    useUnifiedTopology: true,
                    useFindAndModify: false,
                    useCreateIndex: true
                    });
                    let cpdata = new psycho();
                    cpdata.nom = dataObj['nom'];
                    cpdata.activite = dataObj['activite'];
                    cpdata.addresse = dataObj['addresse'];
                    cpdata.telephone = dataObj['telephone'];
                    cpdata.save(function (err) {
                        if (err) console.log("INSERTION FAILED", err);
                        else {
                            // saved!
                            console.log("SAVED");
                        }
                    })
                    //console.log(profileDatatest);
                    //profData.push(profileDatatest);
                    // here push to db
            }
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
                return await scrapeCurrentPages(); // Call this function recursively
            }
            //resolve("profData");
            return profData;
        }
        //for (let i = 0; i < urlCategory.url.length; i++) {
                //pageCount = 1;
                await page.goto(urlCategory.url, {waitUntil: 'domcontentloaded', timeout: 300000});
                await scrapeCurrentPages(); //block loop for too long
        //}
        //resolve("profData");
        await page.close();
        /*let data = await scrapeCurrentPages();
        return data;*/
        console.log("done");
        //await jsonExport(profData);
        return 0;
    }
}

module.exports = scraperObject;