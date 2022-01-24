const fs = require('fs');

const utilities = {
    async delay(time) {
        return new Promise(function(resolve) { 
            setTimeout(resolve, time)
        });
    },
    async jsonExport(scrapedCatData, filename) {
        // put json object in a file
        try {
            await fs.readFile(filename, async function (err, data) {
                let json = await JSON.parse(data);
                await json.push(scrapedCatData);
                await utilities.delay(1000);

                await fs.writeFile(filename, JSON.stringify(json), async function(err){
                if (err) throw err;
                console.log('The "data to append" was appended to file!');
                });
                await utilities.delay(300);
            })
        } catch (err) {
            console.log(err);
        }
    }
};

module.exports = utilities;