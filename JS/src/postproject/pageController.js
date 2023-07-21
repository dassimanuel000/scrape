const pageScraper = require('./pageScrapper');
const connectToEnt = require('./connect');

process.setMaxListeners(0);  

async function scrapeAll(browserInstance){
    let browser;
    try{
        browser = await browserInstance;
        //let page = await browser.newPage();
        //await connectToEnt.connectiontoEnt(page);
        //await pageScraper.scraper(page);
    }
    catch(err){
        console.log("Could not resolve the browser instance => ", err);
    }
}

module.exports = (browserInstance) => scrapeAll(browserInstance);