const browserObject = require('./browser');
const scraperController = require('./pageController');
  
//Start the browser and create a browser instance
function posterBegin(){
let browserInstance = browserObject.startBrowser();
return browserInstance;
}
// Pass the browser instance to the scraper controller
scraperController(posterBegin());