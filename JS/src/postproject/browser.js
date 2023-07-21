const puppeteer = require('puppeteer-extra')
const StealthPlugin = require('puppeteer-extra-plugin-stealth')
const vanillaPuppeteer = require('puppeteer');
const puppeteerExtraPluginUserAgentOverride = require('puppeteer-extra-plugin-stealth/evasions/user-agent-override');
const {addExtra} = require('puppeteer-extra');
const { Cluster } = require('puppeteer-cluster3');
const config = require('./config');
const scrapping = require('./pageScrapper.js');
const connect = require('./connect');
const mongoose = require('mongoose');
const annonce = require('./annonce');
var fork = require('child_process').fork;
const prompt = require('prompt-sync')();
let i = null;  

function posterStart(i) {
  var child = fork('src/index.js',[JSON.stringify(i)]);
};

async function delay(time) {
    return new Promise(function(resolve) { 
        setTimeout(resolve, time)
    });
}

async function deleteAllData (bddconection) {
  try {
   await mongoose.connect(bddconection, { // on envois les donn�es sur mongodb
        useNewUrlParser: true,
        useUnifiedTopology: true,
        //useFindAndModify: false,
        //useCreateIndex: true
    }).then((connection) => {
      mongoose.connection.db.dropDatabase();
    });;
    try {
      await annonce.deleteMany();
      console.log('All Data successfully deleted');
    } catch (err) {
      console.log(err+'data deleted successfully');
    }
    } catch(err) {
      console.log(err);
    }
  };

  

puppeteer.use(StealthPlugin())

function startBrowser(index) {
  
  /*    
    i = prompt("Start number in population file   ");
    console.log('Startnumber = '+`${i}`);
    let endNum = prompt("Start number in population file   ");
    console.log('endNum = '+`${endNum}`);
    par = i-1;
    i--;
    */
      
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
      const pluginStealth = StealthPlugin();
      pluginStealth.enabledEvasions.delete('user-agent-override');
      puppeteer.use(StealthPlugin());
      const pluginUserAgentOverride = puppeteerExtraPluginUserAgentOverride({
        locale: config.locale,
        userAgent: config.userAgent,
        platform: config.platform,
        vendor: 'Google Inc. (NVIDIA)',
        renderer: 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.5671)',
        languages: ['fr-FR', 'fr'],
      });
      puppeteer.use(pluginUserAgentOverride);
      const prompt = require('prompt-sync')();
      const cluster = await Cluster.launch({
          puppeteer,
          puppeteerOptions: {
              headless: true, //true means it will launch on top
              slowMo: 120, // slow down puppeteer //max recommend is 250 //minimum 80 //good 150 ?
              args: browserArgs,
              ignoreHTTPSErrors: true,
              defaultViewport: config.viewport
          },
          workerCreationDelay: 500,
          monitor: true,
          concurrency: Cluster.CONCURRENCY_PAGE, //all tabs connect with same cookies
          maxConcurrency: 2, // Scrap 11 pages in 16 minutes ~220 profiles with 4 workers
          timeout: 2147483640, // Keep a ,
      });

      // Event handler to be called in case of problems
      cluster.on('taskerror', (err, data) => {
          console.log(`Error crawling ${data}: ${err.message}`);
      });
      //let pageNumber = 0;
        const signInLaunch = async ({ page, data: userInfo }) => { // will sign in and launch the postings
        await delay(2000);
        await connect.connectiontoEnt(page); 
        await delay(1000);
        await scrapping.scrape(page, userInfo); //opens page apec with multi worker          
        await delay(2000);
      };
      

      await cluster.task(async ({ page, data: { data, url },i }) => { //default function enables us to use the works to create all the posts
        //i = prompt("number in population file   ");
        //console.log(`Scrapping the db : mongodb://192.168.1.174/T1C${i}`);
        let index = process.argv[2];                                                                                                                                                                        
        console.log(process.argv[2]);
        try {           
           // console.log("index is " + parseInt(index));                                                                                            
            index = parseInt(index);
            console.log("Check poster 1 starts at " + index);
        } catch (e) {                                                                                               
            console.log('Could not parse string as JSON for poster');                                              
        } 
        console.log(index);
        i = index;
        i--;
        let max = i+10;
         
        console.log("Check poster 2 The variable i equals " + i);

        while (i<max) {
          
          console.log(`Scrapping the db : mongodb://192.168.1.174/T1C${i}`);
          let bddconection = `mongodb://192.168.1.174/T1C${i}`;
            await mongoose.connect(bddconection, { // on envois les données sur mongodb
                    useNewUrlParser: true,
                    useUnifiedTopology: true,
                    //useFindAndModify: false,
                    //useCreateIndex: true
                });
            
            let userInfo = await annonce.find({});
            await delay(2000);//counterUser userInfo.length
            for (let counterUser = 0; counterUser < userInfo.length; counterUser++) {
                console.log("Worker Launch");
                await cluster.queue(userInfo[counterUser], signInLaunch);
                await delay(1000);
            }   
            
            ++i;
            
            try {
              deleteAllData (bddconection);
              mongoose.connection.close();
            } catch {
              console.log('closed data base at '+ i);
            }
            
          }

      });
    //await cluster.queue({ data: 0, url : "https://bot.sannysoft.com" });
    //await cluster.queue({ data: 0, url : "http://www.mon-ip.com" });

      await cluster.queue({ data: "", url : "google.com" }); //adds actions to operations queue
      await cluster.idle();
      posterStart(i);
      await cluster.close();
      //await browser.close();
    })();
  };

module.exports = {
    startBrowser
};
