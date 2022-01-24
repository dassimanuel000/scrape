const mongoose = require('mongoose');
const annonce = require('./annonce');

const utilities = {
    async delay(time) {
        return new Promise(function(resolve) { 
            setTimeout(resolve, time)
        });
    },
    async jsonExport(dataObj) {
        // sends to mongoose 
        try {

                await mongoose.connect('mongodb://localhost/regionjob', { // on envois les données sur mongodb
                    useNewUrlParser: true,
                    useUnifiedTopology: true,
                    //useFindAndModify: false,
                    //useCreateIndex: true
                });
                
                    let thdata = new annonce();
                    thdata.date = dataObj['date'];
                    thdata.url = dataObj['url'];
                    thdata.titre = dataObj['titre'];
                    thdata.company = dataObj['company'];
                    thdata.contrat = dataObj['contrat'];
                    thdata.ville = dataObj['ville'];
                    thdata.activite = dataObj['activite'];
                    thdata.description = dataObj['description'];
                    thdata.posttime = dataObj['postTime'];
                    thdata.salary = dataObj['salary'];
                    thdata.metier = dataObj['metier'];
                    thdata.statut = dataObj['statut'];
                    thdata.secteur = dataObj['secteur'];
                    thdata.experience = dataObj['experience'];
                    thdata.save(function (err) {
                        if (err) console.log("INSERTION FAILED", err);
                        else { // saved!
                            console.log("SAVED");
                        }
                  });
            }//)
        //} 
        catch (err) {
            console.log(err);
        }
    },
};

module.exports = utilities;
