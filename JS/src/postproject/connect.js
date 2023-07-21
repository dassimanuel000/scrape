async function delay(time) {
    return new Promise(function(resolve) { 
        setTimeout(resolve, time)
    });
 }  

const scraperObject = {
    url: 'https://emploi-talent.com/wp-admin/',
    async connectiontoEnt(pageLogin) {
        console.log(`Navigating to ${this.url}...`);
        await pageLogin.goto(this.url);
        await pageLogin.setDefaultNavigationTimeout(0); 
       
        // Wait for the required DOM to be rendered
        try {
        await scrapeCurrentPage();
        } catch {
            console.log("Already Connected");
        }
        async function scrapeCurrentPage(){
        pageLogin.waitForNavigation({ waitUntil: 'networkidle2' });
        await pageLogin.waitForSelector('#login');
       
        await delay(2000);
        await pageLogin.$eval('#user_login', el => el.value = 'AdminSen');
        await pageLogin.$eval('#user_pass', el => el.value = 'ZjR()BlCKKHMnRIr(8');
        await delay(2000);
       
        await pageLogin.click("#wp-submit");
        await delay(2000);
        console.log("connected"); 
    }
    return pageLogin;
    }
}

module.exports = scraperObject;