const vanillaPuppeteer = require('puppeteer');
const puppeteerExtraPluginStealth = require('puppeteer-extra-plugin-stealth');
const puppeteerExtraPluginUserAgentOverride = require('puppeteer-extra-plugin-stealth/evasions/user-agent-override');
const {addExtra} = require('puppeteer-extra');
const { Cluster } = require('puppeteer-cluster3');
const Stealth = require('puppeteer-extra-plugin-stealth');
const utils = require('./utils');
const config = require('./config');
const scrapping = require('./scrapping');
process.setMaxListeners(0);
async function delay(time) {
  return new Promise(function(resolve) { 
      setTimeout(resolve, time)
  });
}  

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
              slowMo: 150, // slow down puppeteer //max recommend is 250 //minimum 80 //good 150 ?
              args: browserArgs,
              ignoreHTTPSErrors: true,
              defaultViewport: config.viewport
          },
          workerCreationDelay: 4000,
          monitor: true,
          concurrency: Cluster.CONCURRENCY_BROWSER, //all tabs connect with same cookies
          maxConcurrency: 30, // Scrap 11 pages in 16 minutes ~220 profiles with 4 workers
          timeout: 2147483640, // Keep a ,
      });

      // Event handler to be called in case of problems
      cluster.on('taskerror', (err, data) => {
          console.log(`Error crawling ${data}: ${err.message}`);
      });
      //let pageNumber = 0;
      const scrapeAnnoncePageJaune = async ({ page, data: url }) => {
          let result = await scrapping.scrapeAnnoncePage(page, url); //opens page apec with multi worker
            
            await utils.jsonExport(result); //writes in Mongodb
      };

      await cluster.task(async ({ page, data: { data, url } }) => {
        /*await page.goto(url, {waitUntil: 'domcontentloaded', timeout: 30000});
        await page.screenshot({path: './screenshot.png'});
        console.log("testurl", url);*/
        let resultLink = await scrapping.scrapeCurrentPage(page); //google page -> get links
        if (resultLink && resultLink.length > 0) {
          pageLinks = resultLink;
          await resultLink.forEach(async table => {  //table of page links
            await table.forEach(async element => { // individual page 
            await cluster.queue(element.toString(), scrapeAnnoncePageJaune); //we scrape each page in order 
            });
          });
          
        }
        return 0;
    });
    //await cluster.queue({ data: 0, url : "https://bot.sannysoft.com" });
    //await cluster.queue({ data: 0, url : "http://www.mon-ip.com" });

      await cluster.queue({ data: "", url : "google.com" }); //adds actions to operations queue
      await cluster.idle();
      await cluster.close();
    })();
  };

module.exports = {
    startBrowser
};
