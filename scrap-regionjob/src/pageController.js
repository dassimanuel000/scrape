//const pageScraper = require('./pageScrapper');
//const connectiontoEnt = require('./connect');
async function scrapeAll(browserInstance){
    let browser;
    try{
        browser = await browserInstance;
        //let cpName = await connectiontoEnt.getCompanyName();//browser);
        //await pageScraper.connectiontoEnt(browser, cpName);

    }
    catch(err){
        console.log("Could not resolve the browser instance => ", err);
    }
}

module.exports = (browserInstance) => scrapeAll(browserInstance);
