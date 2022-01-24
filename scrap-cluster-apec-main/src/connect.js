const excelToJson = require('convert-excel-to-json');
const fs = require('fs');

const scraperObject = {
    async getCompanyName() {
        const result = excelToJson({
            source: fs.readFileSync('./data.xls'),
            sheets: ['etablissements'],
            columnToKey: {
                V: 'firstname',
                AB: 'lastname',
                AP: 'streetNumber',
                AQ: 'bis',
                AT: 'cityCode',
                AS: 'streetName',
                C: 'siret'
            }
        });
    return result;
    }
}

module.exports = scraperObject;
