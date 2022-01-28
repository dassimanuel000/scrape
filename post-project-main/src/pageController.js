const pageScraper = require('./pageScrapper');
const connectToEnt = require('./connect');

async function delay(time) {
    return new Promise(function(resolve) { 
        setTimeout(resolve, time)
    });
 }

async function scrapeAll(browserInstance){
    let browser;
    try{
        browser = await browserInstance;
        await connectToEnt.connectiontoEnt(browser);
        await pageScraper.scraper(browser);

    }
    catch(err){
        console.log("Could not resolve the browser instance => ", err);
    }
}

module.exports = (browserInstance) => scrapeAll(browserInstance);