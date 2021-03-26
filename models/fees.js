var mongoose = require('mongoose');
var Schema      = mongoose.Schema;
var Feesschema = new Schema({
   fees_type: String,
    graduate : String,
    department_type : String,
    semester : String,
    department : String,
    fees_amount : Number
},
{
  collection:'fees_info'
});
Fees = mongoose.model('Fees',Feesschema);
module.exports=Fees;
