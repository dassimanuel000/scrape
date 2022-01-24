const pageScraper = require('./pageScrapper');
async function scrapeAll(browserInstance){
    let browser;
    try{
        browser = await browserInstance;
        //let catUrl = await pageScraper.scraperCat(browser);
        await pageScraper.scraper(browser, catUrl);

    }
    catch(err){
        console.log("Could not resolve the browser instance => ", err);
    }
}

module.exports = (browserInstance) => scrapeAll(browserInstance);