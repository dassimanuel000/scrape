const puppeteer = require('puppeteer');
const puppeteerExtraPluginStealth = require('puppeteer-extra-plugin-stealth');
const puppeteerExtraPluginUserAgentOverride = require('puppeteer-extra-plugin-stealth/evasions/user-agent-override');
const {PuppeteerExtra} = require('puppeteer-extra');
//puppeteer.use(StealthPlugin());

function preload(device) {
    Object.defineProperty(navigator, 'platform', {
      value: device.platform,
      writable: true,
    });
    Object.defineProperty(navigator, 'userAgent', {
      value: device.userAgent,
      writable: true,
    });
    Object.defineProperty(screen, 'height', {
      value: device.viewport.height,
      writable: true,
    });
    Object.defineProperty(screen, 'width', {
      value: device.viewport.width,
      writable: true,
    });
    Object.defineProperty(window, 'devicePixelRatio', {
      value: device.viewport.deviceScaleFactor,
      writable: true,
    });
  }
  
  const device = {
    userAgent: 'Mozilla/5.0 (MacIntel)',
    viewport: {
      width: 1200,
      height: 800,
      deviceScaleFactor: 1,
      isMobile: false,
      hasTouch: false,
      isLandscape: true,
    },
    locale: 'en-US,en;q=0.9',
    platform: 'MacIntel',
  };

// add stealth plugin and use defaults (all evasion techniques)
/*const StealthPlugin = require('puppeteer-extra-plugin-stealth')
puppeteer.use(StealthPlugin())

async function startBrowser(){
    let browser;
    try {
        console.log("Opening the browser......");
        browser = await puppeteer.launch({
            headless: false,
            args: ["--disable-setuid-sandbox"],
            'ignoreHTTPSErrors': true
        });
    } catch (err) {
        console.log("Could not create a browser instance => : ", err);
    }
    return browser;
}*/

function startBrowser() {
    try {
      const pptr = new PuppeteerExtra(puppeteer);
      const pluginStealth = puppeteerExtraPluginStealth();
      pluginStealth.enabledEvasions.delete('user-agent-override'); // Remove this specific stealth plugin from the default set
      pptr.use(pluginStealth);
  
      const pluginUserAgentOverride = puppeteerExtraPluginUserAgentOverride({
        userAgent: device.userAgent,
        locale: device.locale,
        platform: device.platform,
      });
      pptr.use(pluginUserAgentOverride);
  
      const browser = pptr.launch({ //await
        args: [
          '--disable-features=site-per-process',
          `--window-size=${device.viewport.width},${device.viewport.height}`,
          '--flag-switches-begin',
          '--disable-site-isolation-trials',
          '--flag-switches-end'
        ],
        headless: false,
        defaultViewport: device.viewport,
      });
      return browser;
    } catch (err) {
      console.error(err);
    }
  };

module.exports = {
    startBrowser
};