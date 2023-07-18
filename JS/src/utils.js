const mongoose = require('mongoose');
const annonce = require('./annonce');
var fs = require('fs');

const utilities = {
    async delay(time) {
        return new Promise(function(resolve) { 
            setTimeout(resolve, time)
        });
    },
    
    async doclean(str, bool) {
        let cleanstr;
    
        try {
        if (bool) {
            str = str.split(":");
            cleanstr = str[1].replace(/(\r\n|\n|\r)/gm, "");
            cleanstr = cleanstr.replace(/  +/g, ' ');
        } else if (!bool) {
            cleanstr = str.replace(/(\r\n|\n|\r)/gm, "");
            cleanstr = cleanstr.replace(/  +/g, ' ');
        }
        if (cleanstr=="undefined"){
            cleanstr = '';
        }
        return cleanstr;
        } catch (err) {
            console.log("bad str", str);
            return String(str).split('  ').join('').split('\n').join('');
        }
    },
    async saveToMongo(dataObj, metier, cats, region,J,M) {
        const json = JSON.stringify(dataObj);
	
        fs.writeFile(`../stockageOffres${J}-${M}/${metier}--${region}--${cats.split('/')[1]}.json`, json, (err) => {
            if (err) {
                throw err;
            }
            console.log("JSON data is saved.");
        });
    },
};

module.exports = utilities;
