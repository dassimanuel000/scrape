const fs = require('fs');

async function delay(time) {
    return new Promise(function(resolve) { 
        setTimeout(resolve, time)
    });
 }

const scraperObject = {
    url: 'https://freelance-france.com/wp-admin/',
    async scraper(browser) {
        let page = await browser.newPage();
        let rawdata = fs.readFileSync('output.json');
        let userInfo = await JSON.parse(rawdata);
    for (let counterUser = 0; counterUser < userInfo.length; counterUser++) {
        console.log(`Navigating to ${this.url}...`);
        await page.goto(this.url);
        // Wait for the required DOM to be rendered
        async function scrapeCurrentPage(){
        page.waitForNavigation({ waitUntil: 'networkidle2' });
        await page.waitForSelector('#adminmenumain');
        // Get the link to all the required books
        await page.click('#menu-posts-listing > a');
        await delay(1000);
        await page.click('.page-title-action');
        page.waitForNavigation({ waitUntil: 'networkidle2' });
        await delay(8000);
        let info = {
            titre: userInfo[counterUser].titre,
            description: userInfo[counterUser].description,
            addresse: userInfo[counterUser].addresse,
            travail: userInfo[counterUser].travail,
            telephone: userInfo[counterUser].telephone,

        };
        await page.$eval('#titlewrap > input', (el, titre) => el.value = titre, info.titre); //title
        await delay(1000);

        try {
        await page.$eval('#gAddress', (el, addresse) => el.value = addresse, info.addresse); //address
        await page.click('#gAddress');
        await delay(1000);
        await page.click('.pac-container > .pac-item');
        await delay(1000);
        } catch {
        await page.$eval('#gAddress', (el => el.value = "France")); //address
        await delay(1000);
        await page.click('#titlewrap > input');
        await page.click('#gAddress');
        await delay(1000);
        await page.click('.pac-container > .pac-item');
        await delay(1000);
        }

        await page.$eval('#phone', (el, telephone) => el.value = telephone, info.telephone); //phone
        await delay(1000);

        const frames = await page.frames();
        await delay(1000);
        let iframe = await frames.find(f => f.name() === 'content_ifr');
        const textInput = await iframe.$('#tinymce');
        await textInput.focus();
        await page.keyboard.type(info.description);
        await delay(1000);

        let value = await page.$$eval('#listing-category-all > ul > li', catlink => {
            // Extract the links from the data
            catlink = catlink.map(el => {
                let res = el.querySelector('label').innerHTML;
                res = res.replace(/<.*>/, '');
                res = res.substring(1);
                return res; });
            return catlink;
          });
        let cat = ["Projet"]; // if didnt exist remove
        await cat.push(info.travail);
        let count = 0;

        count = 0;
        while (cat[count]) {
            const catHandlers = await page.$x("//label[contains(text(), '"+cat[count]+"')]");

            if (catHandlers.length > 0) {
                await catHandlers[0].click();
            } else {
                console.log("Label not found");
                await delay(1000);
                await page.click('#listing-category-add-toggle');
                await delay(1000);
                await page.$eval('#newlisting-category', (el, category) => el.value = category, cat[count]); // category
                await delay(1000);
                await page.click('#listing-category-add-submit');
                await delay(4000);
            }
            await delay(4000);
            ++count;
        }

        await delay(4000);
        await page.click("#publish");
        await delay(10000);
        }
        let data = await scrapeCurrentPage(); 
        console.log("done");
        }
        return 0;
    }
}

module.exports = scraperObject;