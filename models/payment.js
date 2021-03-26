var mongoose = require('mongoose');
var Schema      = mongoose.Schema;
var Paymentschema = new Schema({
 req_id: String,
 admission_no: String,
 name:String,
 department:String,
 department_type:String,
 semester:String,
 graduate:String,
 validatefees:String,
 fees_type:String
},
{
  collection:'payment_fees'
});
Payment = mongoose.model('Payment',Paymentschema);
module.exports=Payment;
