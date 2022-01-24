const mongoose = require('mongoose');
const Schema = mongoose.Schema;
const ObjectId = Schema.ObjectId;

const todaypsychologs = new Schema({
  id: ObjectId,
  nom: String,
  activite: String,
  addresse: String,
  telephone: String,
});

module.exports = mongoose.model('todaypsycholog', todaypsychologs, 'todaypsycholog');