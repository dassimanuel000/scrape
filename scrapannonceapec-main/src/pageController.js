const pageScraper = require('./pageScrapper');
async function scrapeAll(browserInstance){
    let browser;
    try{
        browser = await browserInstance; // ouvre un navigateur
        await pageScraper.scraper(browser); // commence le scrapping avec la fonction

    }
    catch(err){
        console.log("Could not resolve the browser instance => ", err);
    }
}

module.exports = (browserInstance) => scrapeAll(browserInstance);