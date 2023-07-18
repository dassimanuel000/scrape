const browserObject = require('./browser');
const scraperController = require('./pageController');
const utils = require('./utils');
var exec = require('exec');
const child_process = require('child_process');
const prompt = require('prompt-sync')();
//update population file
//child_process.exec('curl -L "https://docs.google.com/spreadsheets/d/1a9wabH5oSOuzv6fQcR2wkETQu3M5OybyLDH7cPXxT_4/export?gid=0&format=xlsx" > ./Populations.xlsx')

//Start the browser and create a browser instance
numberOffre = 0

let browserInstance = browserObject.startBrowser(numberOffre);
// Pass the browser instance to the scraper controller

scraperController(browserInstance);