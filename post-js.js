const mongoose = require("mongoose");
const annonce = require("./annonce");
let select = require("puppeteer-select");
let set = 0;
async function delay(time) {
  return new Promise(function (resolve) {
    setTimeout(resolve, time);
  });
}

const scraperObject = {
  url: "https://trouver-un-candidat.com/wp-admin/post-new.php?post_type=job_listing",
  async scrape(page, userInfo) {
    //let page = await browser.newPage();
    console.log(`Navigating to ${this.url}...`);
    await page.goto(this.url, {
      waitUntil: "domcontentloaded",
      timeout: 300000,
    });
    await page.setDefaultNavigationTimeout(0);
    // Wait for the required DOM to be rendered
    async function scrapeCurrentPage() {
      //page.waitForNavigation({ waitUntil: 'networkidle2' });
      try {
        await page.click('button[aria-label="Fermez la boite de dialogue"]');
        await delay(2000);
      } catch (err) {
        console.log("no popup");
      }
      //aria-label="Fermez la boite de dialogue"
      await page.waitForSelector(".interface-interface-skeleton__body");
      try {
        if (userInfo.ville == null) {
          userInfo.ville = userInfo.contrat;
        }
        userInfo.ville = await userInfo.ville.trim(); //remove space
        let title = String(userInfo.titre) + " " + String(userInfo.ville);
        userInfo.description = await cleaner(userInfo.description); // trying to correct the many many mistakes from description formating
        let info = {
          date: userInfo.date,
          url: userInfo.url,
          titre: title,
          ville: userInfo.ville,
          description: userInfo.description,
          salary: userInfo.salary,
          experience: userInfo.experience,
          cats: userInfo.cats,
          places: userInfo.places,
        };

        try {
          await delay(2000);
          await page.$eval(
            ".editor-post-title__input",
            (el, titre) => (el.value = titre),
            info.titre
          ); //title
          await page.focus(".editor-post-title__input");
          await page.keyboard.type(info.titre);
          await delay(3000);

          //await page.$eval('.block-editor-block-list__layout', (el, titre) => el.value = titre, info.description); //title
          await page.focus(".block-editor-block-list__layout");
          await page.keyboard.press("Enter"); // Enter Key
          page.keyboard.sendCharacter(info.description);
          await delay(3000);
          /*
        await page.$eval('#_job_salary', (el, titre) => el.value = titre, "1000"); //salary
        await page.$eval('#_job_max_salary', (el, titre) => el.value = titre, "3000"); //salary
        //_job_max_salary
        */
          await page.click("#_job_apply_type");
          await page.focus(".select2-search__field");
          await page.keyboard.type("URL");
          await delay(1000);
          await page.click("#select2-_job_apply_type-results > li");

          await delay(1000);
          await page.$eval(
            "#_job_apply_url",
            (el, titre) => (el.value = titre),
            info.url
          );
          await page.$eval(
            "#_job_address",
            (el, titre) => (el.value = titre),
            info.ville
          );
          await delay(1000);

          await delay(1000);
          await page.click("#_job_experience");
          await delay(1000);

          var experienceNumber = info.experience;
          var experienceCat = experienceNumber.replace(/[^0-9]/g, "");
          if (experienceCat) {
            await page.focus(".select2-search__field");
            await page.keyboard.type(experienceCat);
            await page.click(".select2-results__option");
          } else {
            await page.focus(".select2-search__field");
            await page.keyboard.type("1");
            await page.click(".select2-results__option");
          }

          //await page.$eval('#_job_map_location', (el, titre) => el.value = titre, info.ville);
          await page.focus(".pw-map-search-wrapper > input");
          await page.keyboard.type(info.ville);
          //await page.click('.pw-map-search-wrapper');
          await delay(2000);
          try {
            await page.click(".pac-item > .pac-item-query"); // click on city
          } catch (err) {
            console.log("pas de ville");
            await page.$eval(
              "#_job_address",
              (el, titre) => (el.value = titre),
              "France"
            );
            //await page.$eval('pw-map-search-wrapper', (el, titre) => el.value = titre, "France");
          }

          try {
            let categories = userInfo.cats;
            let mainCat = String(categories.split("/")[0]);
            let secondaryCat = String(categories.split("/")[1]);
            let preciseCat = String(categories.split("/")[2]);
            console.dir(mainCat + " " + secondaryCat + " " + preciseCat);

            let element0 = await select(page).getElement(
              `button:contains(Emploi)`
            );
            await delay(1000);
            await element0.click();
            await delay(2000);

            let element = await select(page).getElement(
              `button:contains(Catégories)`
            );
            await delay(1000);
            await element.click();
            await delay(2000);

            try {
              let element1 = await select(page).getElement(
                `label:contains(${mainCat})`
              );
              await element1.click();
              await delay(3000);
            } catch (err) {
              console.log(err);
              await delay(2000);
              await element.click();
              await delay(2000);
              let element1 = await select(page).getElement(
                `label:contains(${mainCat})`
              );
              await element1.click();
              await delay(3000);
            }
            let element2 = await select(page).getElement(
              `label:contains(${secondaryCat})`
            );
            await element2.click();
            await delay(2000);
            let element3 = await select(page).getElement(
              `label:contains(${preciseCat})`
            );
            await element3.click();
            let element9 = await select(page).getElement(
              `button:contains(Catégories)`
            );
            await element9.click();
            await delay(2000);
          } catch (err) {
            console.log(err);
          }
          try {
            let location = userInfo.places;
            let mainLoca = String(location.split("/")[0]);
            let secondaryLoca = String(location.split("/")[1]);
            let preciseLoca = String(location.split("/")[2]);
            console.dir(mainLoca + " " + secondaryLoca + " " + preciseLoca);
            await delay(2000);

            let element4 = await select(page).getElement(
              `button:contains(Lieux)`
            );
            await element4.click();
            await delay(3000);
            try {
              let element5 = await select(page).getElement(
                `label:contains(${mainLoca})`
              );
              await element5.click();
            } catch {
              await element4.click();
              let element5 = await select(page).getElement(
                `label:contains(${mainLoca})`
              );
              await element5.click();
            }
            await delay(3000);
            let element6 = await select(page).getElement(
              `label:contains(${secondaryLoca})`
            );
            await element6.click();
            await delay(2000);
            let element7 = await select(page).getElement(
              `label:contains(${preciseLoca})`
            );
            await element7.click();
            await delay(2000);
            await element4.click();
            await delay(2000);
          } catch (err) {
            console.log(err);
          }
        } catch (err) {
          console.log("erreur", err);
        }
        // save
        await delay(1000);
        try {
          let element = await select(page).getElement(
            `button:contains(Publier)`
          );
          await element.click();
          await delay(3000);
          let element1 = await select(page).getElement(
            `button:contains(Publier)`
          );
          await element1.click();
          await delay(3000);
        } catch (err) {
          console.log("erreur : ", err);
          await page.click(".editor-post-save-draft"); // click on city
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
  },
};

async function cleaner(str) {
  let breaker = [
    "Descriptif du poste",
    "Compï¿½tences requises :",
    "Profil recherchï¿½",
    "Qualitï¿½s requisesï¿½:",
    "Autres offres de l'entreprise",
    "Processus de recrutement",
    "Personne en charge du recrutement",
    "Entreprise",
  ];
  for (let i = 0; i < breaker.length; ++i) {
    if (str.search(breaker[i]) == 0) {
      str = str.split(String(breaker[i])).join(breaker[i] + " \n");
    }
    if (str.search(breaker[i]) != -1 && str.search(breaker[i]) > 0) {
      //console.log(str.search(breaker[i]));
      str = str.split(String(breaker[i])).join("\n " + breaker[i] + " \n");
    }
  }
  str = str.split(".").join(". ");
  str = str.split("-").join("\n");
  return str;
}

module.exports = scraperObject;
