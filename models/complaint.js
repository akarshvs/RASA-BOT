var mongoose = require('mongoose');
var Schema      = mongoose.Schema;
var Studentschema = new Schema({

    complaint : String,

},
{
  collection:'complaint'
});
Complaint = mongoose.model('Complaint',Studentschema);
module.exports=Complaint;
