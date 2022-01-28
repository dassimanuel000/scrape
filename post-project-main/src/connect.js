async function delay(time) {
    return new Promise(function(resolve) { 
        setTimeout(resolve, time)
    });
 }

const scraperObject = {
    url: 'https://freelance-france.com/wp-admin/',
    async connectiontoEnt(browser) {
        let pageLogin = await browser.newPage();
        console.log(`Navigating to ${this.url}...`);
        await pageLogin.goto(this.url);
        // Wait for the required DOM to be rendered
        await scrapeCurrentPage();
        async function scrapeCurrentPage(){
        pageLogin.waitForNavigation({ waitUntil: 'networkidle2' });
        await pageLogin.waitForSelector('#login');

        await delay(1000);
        await pageLogin.$eval('#user_login', el => el.value = 'AdminFreelanceFrance');
        await pageLogin.$eval('#user_pass', el => el.value = '^hTumI$(dC1RaNdx30!vF)Ew');
        await delay(2000);
        await pageLogin.click("#wp-submit");
        await delay(4000);

        await pageLogin.close();
        return 0;
    }
    console.log("connected");
    return 0;
    }
}

module.exports = scraperObject;