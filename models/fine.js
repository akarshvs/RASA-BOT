var mongoose = require('mongoose');
var Schema      = mongoose.Schema;
var Fineschema = new Schema({
   fees_type: String,
    graduate : String,
    department_type : String,
    semester : String,
    last_date : String,
    fine : String,
    superfine : String,
    superfine_date : String,
},
{
  collection:'fees_date_fine'
});
Fine = mongoose.model('Fine',Fineschema);
module.exports=Fine;
