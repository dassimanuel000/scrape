const vanillaPuppeteer = require('puppeteer');
const puppeteerExtraPluginStealth = require('puppeteer-extra-plugin-stealth');
const puppeteerExtraPluginUserAgentOverride = require('puppeteer-extra-plugin-stealth/evasions/user-agent-override');
const {addExtra} = require('puppeteer-extra');
const { Cluster } = require('puppeteer-cluster3');
const Stealth = require('puppeteer-extra-plugin-stealth');
const utils = require('./utils');
const config = require('./config');
const scrapping = require('./scrapping');
const connect = require('./connect');
const mongoose = require('mongoose');
const annonce = require('./annonce');
var fork = require('child_process').fork;
process.setMaxListeners(0);
var i = null, y = null, par = null;
const xlsxFile = require('read-excel-file/node');
const prompt = require('prompt-sync')();

function posterStart(i) {
  var child = fork('src/postproject/index.js',[i]);
  return(Number(i));
};

//const poster = require('../src/postproject/index');

function startBrowser() {
    (async () => {
      let browserArgs = [
          '--disable-infobars',
          '--window-position=0,0',
          '--ignore-certifcate-errors',
          '--ignore-certifcate-errors-spki-list',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          '--disable-features=site-per-process',
          '--hide-scrollbars',
          //'--proxy-server=127.0.0.1:8000',
          '--no-sandbox',
          '--no-zygote',
          '--disable-accelerated-2d-canvas',
          '--disable-gpu',
          `--window-size=${config.viewport.width},${config.viewport.height}`,
          '--flag-switches-begin',
          '--disable-site-isolation-trials',
          '--flag-switches-end',
      ];

      const puppeteer = addExtra(vanillaPuppeteer);
      const pluginStealth = puppeteerExtraPluginStealth();
      pluginStealth.enabledEvasions.delete('user-agent-override');
      puppeteer.use(Stealth());
      const pluginUserAgentOverride = puppeteerExtraPluginUserAgentOverride({
        locale: config.locale,
        userAgent: config.userAgent,
        platform: config.platform,
        vendor: 'Google Inc. (NVIDIA)',
        renderer: 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.5671)',
        languages: ['fr-FR', 'fr'],
      });
      puppeteer.use(pluginUserAgentOverride);

      const cluster = await Cluster.launch({
          puppeteer,
          puppeteerOptions: {
              headless: true, //false
              slowMo: 120, // slow down puppeteer //max recommend is 250 //minimum 80 //good 150 ?
              args: browserArgs,
              ignoreHTTPSErrors: true,
              defaultViewport: config.viewport
          },
          workerCreationDelay: 4000,
          monitor: true,
          concurrency: Cluster.CONCURRENCY_BROWSER, //all tabs connect with same cookies
          maxConcurrency: 5, // Scrap 11 pages in 16 minutes ~220 profiles with 4 workers
          timeout: 2147483640, // Keep a ,
      });
      

      // Event handler to be called in case of problems
      cluster.on('taskerror', (err, data) => {
          console.log(`Error crawling ${data}: ${err.message}`);
      });

      const signInLaunch = async ({ page, data: userInfo }) => { // will sign in and launch the postings
        await utils.delay(2000);
        await connect.connectiontoEnt(page); 
        await utils.delay(1000);
        await posting.scrape(page, userInfo); //opens page apec with multi worker          
        await utils.delay(2000);
      };

      //let pageNumber = 0;
      const saveAnnonceApec = async ({ page, data: url }) => {
          let object = await scrapping.scrapeAnnoncePageApec(page,i, y, String(url)); //opens page apec with multi worker
            
            await utils.saveToMongo(object,i); //writes in Mongodb
      };
      const saveAnnonceRegionJob = async ({ page, data: url }) => {
        let object = await scrapping.scrapeAnnoncePageRegionJob(page,i,y, url); //opens page apec with multi worker
          
          await utils.saveToMongo(object); //writes in Mongodb
      };
      const saveAnnoncePE = async ({ page, data: url }) => {
        let object = await scrapping.scrapeAnnoncePagePe(page,i,y, url); //opens page apec with multi worker
          if (object != 0) {
            await utils.saveToMongo(object,i); //writes in Mongodb
          }
      };
      const saveAnnonceHelloWork = async ({ page, data: url }) => {
        let object = await scrapping.scrapeAnnoncePageHelloWork(page,i,y, url); //opens page apec with multi worker
        if (object != 0) {
          await utils.saveToMongo(object,i); //writes in Mongodb
        }
      };
      const saveAnnoncEmploisenior = async ({ page, data: url }) => {
        let object = await scrapping.scrapeAnnoncePageAnnonctpjob(page,i,y, url); //opens page apec with multi worker
        if (object != 0) {
          await utils.saveToMongo(object,i); //writes in Mongodb
        }
      };
      let ctr = 0;
      const saveAnnoncejobup = async ({ page, data: url }) => {
        ++ctr;
        let object = await scrapping.scrapeAnnoncePagejobupjob(page,i,y,ctr, url); //opens page apec with multi worker
        if (object != 0) {
          await utils.saveToMongo(object,i); //writes in Mongodb
        }
      };
      async function launcher(page,i,y){
        if(i==0){
          return;
        }
        /* PE */
        let peResultLink = await scrapping.scrapeCurrentPagePe(page,i,y); //google page -> get links
          if (peResultLink && peResultLink.length > 0) {
            pageLinks = peResultLink;
            await peResultLink.forEach(async table => {  //table of page links
              await cluster.queue(table.toString(), saveAnnoncePE); //we scrape each page in order 
          });
        }
        
       /* */
    //helloWork
        let HelloWorkResultLink = await scrapping.scrapeLinkPagehellowork(page,i,y); //google page -> get links
          if (HelloWorkResultLink && HelloWorkResultLink.length > 0) {
            pageLinks = HelloWorkResultLink;
            await HelloWorkResultLink.forEach(async table => {  //table of page links
            // await table.forEach(async element => { // individual page 
                await cluster.queue(table.toString(), saveAnnonceHelloWork); //we scrape each page in order 
            // });
            });
        }
        
        /* */
        //apec scraper
        let apecResultLink = await scrapping.scrapeLinkPageApec(page,i,y); //google page -> get links
        if (apecResultLink && apecResultLink.length > 0) {
          pageLinks = apecResultLink;
          await apecResultLink.forEach(async table => {  //table of page links
            await table.forEach(async element => { // individual page 
              await cluster.queue(element.toString(), saveAnnonceApec); //we scrape each page in order 
            });
          });
        }

        /* 
        //jobup scraper 
        let jobupResultLink = await scrapping.scrapeLinkPagejobup(page,i,y); //google page -> get links
        if (jobupResultLink && jobupResultLink.length > 0) {
          pageLinks = jobupResultLink;
          await jobupResultLink.forEach(async table => {  //table of page links
            //await table.forEach(async element => { // individual page 
              await cluster.queue(table.toString(), saveAnnoncejobup); //we scrape each page in order 
            //});
          });
        }
       */
      }
      await cluster.task(async ({ page, data: { data, url } }) => {
          /*  
        //apec scraper
        let apecResultLink = await scrapping.scrapeLinkPageApec(page); //google page -> get links
        if (apecResultLink && apecResultLink.length > 0) {
          pageLinks = apecResultLink;
          await apecResultLink.forEach(async table => {  //table of page links
            await table.forEach(async element => { // individual page 
              await cluster.queue(element.toString(), saveAnnonceApec); //we scrape each page in order 
            });
          });
        }
          */
        
        //regionjob scraper
        i = prompt("Start number in population file   ");
        console.log('Startnumber = '+`${i}`);
        let endNum = i;//prompt("Start number in population file   ");
        //console.log('endNum = '+`${endNum}`);
        //par = i;
        i--; //-1 because of title in "population"
        y = 1;
        await launcher(page,i,y);
        /*prompt("choose job to scrape");
        console.log('job selected is n° '+`${y}`);
        */
      //for (;i<=endNum;i++){
        /*
        let k  = prompt("Start to scrap line "+ i + ' : ');
        if(k==0){
          return;
        }
        */
        /*
        //France Emploi Scrapper
        let regionJobResultLink = await scrapping.scrapeLinkPageRegionJob(page,i,y); //google page -> get links
        if (regionJobResultLink && regionJobResultLink.length > 0) {
          pageLinks = regionJobResultLink;
          await regionJobResultLink.forEach(async table => {  //table of page links
            await table.forEach(async element => { // individual page 
              await cluster.queue(element.toString(), saveAnnonceRegionJob); //we scrape each page in order 
            });
          });
        }
        */
      //pole emploi scraper
        
        

        /*
        //emploisenior
        let emploiseniorResultLink = await scrapping.scrapeLinktpjb(page,i,y); //google page -> get links
        if (emploiseniorResultLink && emploiseniorResultLink.length > 0) {
          pageLinks = emploiseniorResultLink;
          await emploiseniorResultLink.forEach(async table => {  //table of page links
            await cluster.queue(table.toString(), saveAnnoncEmploisenior); //we scrape each page in order 
          });
        }
        */
      //}
});
    //await cluster.queue({ data: 0, url : "https://bot.sannysoft.com" });
    //await cluster.queue({ data: 0, url : "http://www.mon-ip.com" });
      await cluster.queue({ data: "", url : "google.com" }); //adds actions to operations queue
      await cluster.idle();
      posterStart();
      await cluster.close();
    })();
  };



module.exports = {
  startBrowser
};