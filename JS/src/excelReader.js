// var workbook = XLSX.readFile(".// Import dependencies
const fs = require("fs");
const XLSX = require("xlsx");


// Read the file into memory
// sheetRows: 50 pour le test
const workbook = XLSX.readFile("./Populations.xlsx", {cellDates: true});

// Convert the XLSX to JSON
// var listeMetier = [];
// var listeCategories = [];
// var listeLieuTresPrecis = [];
// var listeDepartement = [];
var worksheets = {};
let arrOfArr = [];
const getData = {
    createMyFolder(J, M) {
        const folderName = `../stockageOffres${J}-${M}`
        try {
            if (!fs.existsSync(folderName)) {
              fs.mkdirSync(folderName);
            }
          } catch (err) {
            console.error(err);
            console.log('Dossier déja existant')
          }
        return folderName;
    },
    getMyData(J, M) {
    for (const sheetName of workbook.SheetNames) {
        worksheets[sheetName] = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName]);
    }
   
    for (const candidat of worksheets.ET){
        try{ var date = new Date(candidat["Date de Post"]);} catch (error) {var date = "Pas de date renseignée"};
        try{ var dateString = new Date(date.getTime() - (date.getTimezoneOffset() * 60000 ))
                        .toISOString()
                        .split("T")[0]; } catch (error) { var dateString = 'Date non renseignée' }
        if (dateString == `2023-${M}-${J}`) {
            let singlearr = [];
            singlearr.push(candidat['Département / GV']);
            // listeDepartement.push(candidat['Département / GV']);
            singlearr.push(candidat['Lieu Très Précis']);
            // listeLieuTresPrecis.push(candidat['Lieu Très Précis']);
            singlearr.push(candidat['Profession 1']);
            // listeMetier.push(candidat['Profession 1']);
            singlearr.push(candidat['Catégories']);
            // listeCategories.push(candidat['Catégories']);
            arrOfArr.push(singlearr);
            // console.log(arrOfArr);
        }
    }
    this.createMyFolder(J,M);
    //console.log(arrOfArr);
    return arrOfArr;
    },
    
};


module.exports = getData;

// console.log(listeMetier);
// console.log(listeLieuTresPrecis[0]);
// console.log(listeCategories);
// var obj = JSON.parse(worksheets.T1C)

// console.log(String(obj["Date de Post"]))
// console.log(workbook);