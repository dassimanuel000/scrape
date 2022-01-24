const vanillaPuppeteer = require('puppeteer');
const puppeteerExtraPluginStealth = require('puppeteer-extra-plugin-stealth');
const puppeteerExtraPluginUserAgentOverride = require('puppeteer-extra-plugin-stealth/evasions/user-agent-override');
const RecaptchaPlugin = require('puppeteer-extra-plugin-recaptcha')
const {addExtra} = require('puppeteer-extra');
const { Cluster } = require('puppeteer-cluster3');
const Stealth = require('puppeteer-extra-plugin-stealth');
const utils = require('./utils');
const config = require('./config');
const pageScraper = require('./pageScrapper');
process.setMaxListeners(0);

function startBrowser() {
    (async () => {
      let browserArgs = [
          '--disable-infobars',
          '--window-position=0,0',
          '--ignore-certifcate-errors',
          '--ignore-certifcate-errors-spki-list',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          //'--shm-size=3gb',
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
      /*puppeteer.use(
        RecaptchaPlugin({
          provider: {
            id: '2captcha',
            token: '432b8238524f90c03c3fb24b1a9f700d' // REPLACE THIS WITH YOUR OWN 2CAPTCHA API KEY
          },
          visualFeedback: true // colorize reCAPTCHAs (violet = detected, green = solved)
        })
      )*/
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
              headless: true, //true
              slowMo: 100, // slow down puppeteer //max recommend is 250 //minimum 80 //good 150 ?
              args: browserArgs,
              ignoreHTTPSErrors: true,
              defaultViewport: config.viewport
          },
          workerCreationDelay: 2000,
          monitor: true,
          concurrency: Cluster.CONCURRENCY_BROWSER,
          timeout: 800000000,
          maxConcurrency: 10,
      });

      // Event handler to be called in case of problems
      cluster.on('taskerror', (err, data) => {
          console.log(`Error crawling ${data}: ${err.message}`);
      });

      const scrapCat = async ({ page, data: url }) => {
        try {
          //await connect.connectiontoEnt(page);
          let catUrl = await pageScraper.scraperCat(page);
          for (let index = 0; index < catUrl.length; index++) {
            await cluster.queue({url:catUrl[index]});
            //await pageScraper.scraper(page, catUrl[index]);
        }
        } catch (err) {console.log("error", err);}
          return 0;
      };

      await cluster.task(async ({page, data: url}) => {
        try {
          await pageScraper.scraper(page, url);
        } catch (err) {"error", err}
        return 0;
    });
    //await cluster.queue({ data: 0, url : "https://bot.sannysoft.com" });
    //await cluster.queue({ data: 0, url : "http://www.mon-ip.com" });
    await cluster.queue("http://www.mon-ip.com", scrapCat);

      await cluster.idle();
      await cluster.close();
    })();
  };

module.exports = {
    startBrowser
};