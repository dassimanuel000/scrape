const mongoose = require('mongoose');
const Schema = mongoose.Schema;
const ObjectId = Schema.ObjectId;

//const apec_annonce_cdi = new Schema({ // model pour définir les champs a stocker et dans quel model de la DB
const regionjob_annonce = new Schema({ // model pour définir les champs a stocker et dans quel model de la DB

  id: ObjectId,
  date: String,
  url: {type:String, unique:true}, // helps us evade duplicate postings
  titre: String,
  company: String,
  contrat: String,
  ville: String,
  activite: String,
  description: String,
  posttime: String,
  salary: String,
  experience: String,
  metier: String,
  statut: String,
  secteur: String,
  cats: String,
  places:String,
});

//module.exports = mongoose.model('apec_annonce_cdi', apec_annonce_cdi, 'apec_annonce_cdi');
module.exports = mongoose.model('regionjob_annonce', regionjob_annonce, 'regionjob_annonce');
