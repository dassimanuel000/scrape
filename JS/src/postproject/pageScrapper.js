const mongoose = require('mongoose');
const annonce = require('./annonce');
let select = require ('puppeteer-select');
let set = 0;
async function delay(time) {
    return new Promise(function(resolve) { 
        setTimeout(resolve, time)
    });
 }  

const scraperObject = {
    
    url: 'https://emploi-talent.com/wp-admin/post-new.php?post_type=job_listing',
    async scrape(page, userInfo) {
        //let page = await browser.newPage();
        console.log(`Navigating to ${this.url}...`);
        await page.goto(this.url, {waitUntil: 'domcontentloaded', timeout: 300000});
        await page.setDefaultNavigationTimeout(0); 
        // Wait for the required DOM to be rendered
        async function scrapeCurrentPage(){
        //page.waitForNavigation({ waitUntil: 'networkidle2' });
        try {
            await page.click('button[aria-label="Fermez la boite de dialogue"]');
            await delay(2000);
        }catch (err) {console.log("no popup");}
        //aria-label="Fermez la boite de dialogue"
        await page.waitForSelector('.interface-interface-skeleton__body');
        try {
            if(userInfo.ville==null) {
                userInfo.ville = userInfo.contrat;
            }
            userInfo.ville = await userInfo.ville.trim(); //remove space
            var today = new Date();
		var date = (today.getMonth() + 1) + "" + today.getDate() + "" + today.getSeconds();
            let title = String(userInfo.titre)+ ' '+ String(userInfo.ville)+ ' '+ date;
            userInfo.description = await cleaner(userInfo.description); // trying to correct the many many mistakes from description formating
        let info = {
            date: userInfo.date,
            url: userInfo.url,
            titre: title,
            ville: userInfo.ville, 
            description: userInfo.description,
            salary: userInfo.salary,
            experience: userInfo.experience,
            cats:userInfo.cats,
            places:userInfo.places,
        };
        await delay(4000);
        try {
            try {
                let categories = userInfo.cats;
                let mainCat = String(categories.split('/')[0]);
                let secondaryCat = String(categories.split('/')[1]);
                let preciseCat = String(categories.split('/')[2]);
                console.dir(mainCat+ ' '+secondaryCat+' '+preciseCat);
                
                await delay(2000);
                let element = await select(page).getElement(`button:contains(Categories)`);
                let vt = 0;
                try {
                    await delay(1000);
                    let elementmc = await select(page).getElement(`label:contains(${mainCat})`);
                    await delay(1000);
                    
                    try {
                        try {
                            if(vt==1){
                                let elementmc = await select(page).getElement(`label:contains(${mainCat})`);
                                await delay(1000);
                                await elementmc.focus();
                                await page.keyboard.press('Space');
                            }
                        } catch {
                            console.log("mainCat failed 1")
                        }
                        try{
                            let elementsc = await select(page).getElement(`label:contains(${secondaryCat})`);
                            await delay(1000);
                            await elementsc.focus();
                            await page.keyboard.press('Space');
                        } catch {
                            console.log("scCat failed 1")
                        }
                        try {
                            let elementpc = await select(page).getElement(`label:contains(${preciseCat})`);
                            await delay(1000);
                            await elementpc.focus();
                            await page.keyboard.press('Space');
                        } catch {
                            console.log("preciseCat failed 1")
                        }
                        console.log("Cats 1 successful")
                    } catch {
                        console.log("Cats not already deployed 1");
                        console.log("Opening cats after failing 1")
                
                        await elementmc.focus();
                        await page.keyboard.press('Space');
                        try {
                            try{
                                if(vt==1){
                                    let elementmc = await select(page).getElement(`label:contains(${mainCat})`);
                                    await delay(1000);
                                    await elementmc.focus();
                                    await page.keyboard.press('Space');
                                }
                            } catch {
                                console.log("mainCat failed 2")
                            }
                            try{
                                let elementsc = await select(page).getElement(`label:contains(${secondaryCat})`);
                                await delay(1000);
                                await elementsc.focus();
                                await page.keyboard.press('Space');
                            } catch {
                                console.log("scCat failed 2")
                            }
                            try {
                                let elementpc = await select(page).getElement(`label:contains(${preciseCat})`);
                                await delay(1000);
                                await elementpc.focus();
                                await page.keyboard.press('Space');
                            } catch {
                                console.log("preciseCat failed 2")
                            }
                        } catch {
                            console.log("Cats not already deployed 2")
                        }
                    }
                }   catch {
                    console.log("Cats deployed failed")
                }
                await delay(3000);
                
                let location = userInfo.places;
                let mainLoca = String(location.split('/')[0]);
                let secondaryLoca = String(location.split('/')[1]);
                let preciseLoca = String(location.split('/')[2]);
                console.dir(mainLoca+ ' '+secondaryLoca+' '+preciseLoca);
                element4 = await select(page).getElement(`button:contains(Adresse)`);

                let ve = 0;
                try {
                    await delay(2000);
                    let elementmc = await select(page).getElement(`label:contains(${mainLoca})`);
                    await delay(1000);
                    await elementmc.focus();
                    await page.keyboard.press('Space');
                }   catch {
                    console.log("Cats deployed failed")
                    element = await select(page).getElement(`button:contains(Adresse)`);
                    await delay(500);
                    await element.focus();
                    await element.click();
                    await delay(1000);
                    ++ve;
                }
                try {
                    try {
                        if(ve==1){
                            await delay(2000);
                            let elementmc = await select(page).getElement(`label:contains(${mainLoca})`);
                            await delay(1000);
                            await elementmc.focus();
                            await page.keyboard.press('Space');
                            if(mainLoca=='Télétravail'){
                                ++ve;
                                throw 'télétravail';
                            }
                        }
                    } catch {
                        if(ve==2){
                            throw 'télétravail';
                        }
                        console.log("mainLoca failed")
                    }
                    try{
                        let elementsc = await select(page).getElement(`label:contains(${secondaryLoca})`);
                        await delay(1000);
                        await elementsc.focus();
                        await page.keyboard.press('Space');
                        if(secondaryLoca==undefined){
                            ++ve;
                            throw 'undefined';
                        }
                        await page.focus(element);
                    }catch {
                        console.log("secondaryLoca failed")
                    }
                    try{
                        let elementpc = await select(page).getElement(`label:contains(${preciseLoca})`);
                        await delay(1000);
                        await elementpc.focus();
                        if(preciseLoca=='undefined'){
                            ++ve;
                            throw 'undefined';
                        }
                        if(elementpc){
                        await page.keyboard.press('Space');
                        }
                    } catch {
                        console.log("preciseLoca failed")
                    }
                } catch {
                    console.log("Cats already deployed")
                }
            } catch {
                    console.log("Failure");
            }
        
        await delay(1000);
        //await page.$eval('h1', (el, titre) => el.value = titre, info.titre); //h1 > span
        //await page.waitForSelector('h1[aria-label="Intitulé du poste"]')
        //await page.focus('h1[aria-label="Intitulé du poste"]')  document.querySelector("#editor > div > div.edit-post-layout.is-mode-visual.is-sidebar-opened.has-metaboxes.interface-interface-skeleton.has-footer > div.interface-interface-skeleton__editor > div.interface-interface-skeleton__body > div.interface-navigable-region.interface-interface-skeleton__content > div.edit-post-visual-editor > div.edit-post-visual-editor__content-area > div > div.editor-styles-wrapper.block-editor-writing-flow > div.edit-post-visual-editor__post-title-wrapper.is-layout-flow > h1")
        console.log("Writing title");
        //await page.waitForSelector('.wp-block-post-title')
        await page.focus('.wp-block-post-title')
        //await page.focus('.wp-block-post-title')
        await delay(2000)
        await page.focus('.wp-block-post-title')
        await page.keyboard.type(info.titre.split("undefined").join('').replace(/(\r\n|\n|\r)/gm, ""));
        await delay(3000);
        //await page.keyboard.press('Enter');
        
        //await page.$eval('.block-editor-block-list__layout', (el, titre) => el.value = titre, info.description); //title
        await page.focus('.block-editor-block-list__layout');
        await page.keyboard.press('Enter'); // Enter Key
        page.keyboard.sendCharacter(info.description);
        await delay(3000);
        /*
        await page.$eval('#_job_salary', (el, titre) => el.value = titre, "1000"); //salary
        await page.$eval('#_job_max_salary', (el, titre) => el.value = titre, "3000"); //salary
        //_job_max_salary
        */
        await page.click('#_job_apply_type');
        await page.focus('.select2-search__field');
        await page.keyboard.type("URL");
        await delay(1000);
        await page.click('#select2-_job_apply_type-results > li');
        
        await delay(1000);
        await page.$eval('#_job_apply_url', (el, titre) => el.value = titre, info.url);
        await page.$eval('#_job_address', (el, titre) => el.value = titre, info.ville);
        await delay(1000);
        
        await delay(1000);
        await page.click('#_job_experience');
        await delay(1000);
        
        var experienceNumber = info.experience;
        var experienceCat = experienceNumber.replace(/[^0-9]/g, '');
        if(experienceCat) {
            await page.focus('.select2-search__field');
            await page.keyboard.type(experienceCat);
            await page.click('.select2-results__option');
        } else {
            await page.focus('.select2-search__field');
            await page.keyboard.type("1");
            await page.click('.select2-results__option');
        }
        
        //await page.$eval('#_job_map_location', (el, titre) => el.value = titre, info.ville);
        await page.focus('.pw-map-search-wrapper > input');
        await page.keyboard.type(info.ville);
        //await page.click('.pw-map-search-wrapper');
        /*
        await delay(2000);
        try {
            await page.click('.pac-item > .pac-item-query'); // click on city
        } catch (err) {console.log("pas de ville");
            await page.$eval('#_job_address', (el, titre) => el.value = titre, "France");
        //await page.$eval('pw-map-search-wrapper', (el, titre) => el.value = titre, "France");
        }
        */
        
        } catch (err) {
            console.log("erreur", err);
        }
        // save
        await delay(1000);
        try {
            let element = await select(page).getElement(`button:contains(Publier)`);
                await element.click()
                await delay(3000);
                let element1 = await select(page).getElement(`button:contains(Publier)`);
                await element1.click()
                await delay(3000);
        }catch (err) {
            console.log("erreur : ", err);
            await page.click('.editor-post-save-draft'); // click on city
        }
        await delay(2000);
        } catch (err) {
            console.log("erreur : ", err);
        }
        //page.close();
    } // close page before reopen a new one //
        await scrapeCurrentPage();
        console.log("done");
        return 0;
    }
}

async function cleaner(str){ 
    let breaker = [
    "Descriptif du poste",
    "Compï¿½tences requises :",
    "Profil recherchï¿½",
    "Qualitï¿½s requisesï¿½:",
    "Autres offres de l'entreprise",
    "Processus de recrutement",
    "Personne en charge du recrutement",
    "Entreprise"
    ];
    for (let i = 0; i < breaker.length; ++i){
        if(str.search(breaker[i])==0){
            str = str.split(String(breaker[i])).join(breaker[i]+' \n'); 
        }
        if(str.search(breaker[i])!=-1 && str.search(breaker[i])>0){
            //console.log(str.search(breaker[i]));
            str = str.split(String(breaker[i])).join('\n '+breaker[i]+' \n');
        }
    }
    str = str.split('.').join('. ');
    str = str.split('-').join('\n');
    return str;
}

module.exports = scraperObject;