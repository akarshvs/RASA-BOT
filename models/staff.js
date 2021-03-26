var mongoose = require('mongoose');
var Schema      = mongoose.Schema;
var Staffschema = new Schema({
    name : String,
    position : String,
    department : String,
    contact : String
},
{
  collection:'employee_info'
});
Staff = mongoose.model('Staff',Staffschema);
module.exports=Staff;
