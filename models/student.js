var mongoose = require('mongoose');
var Schema      = mongoose.Schema;
var Studentschema = new Schema({
   admission_no: Number,
    name : String,
    department : String,
    graduate : String,
    department_type : String,
    semester : String
},
{
  collection:'student_info'
});
Student = mongoose.model('Student',Studentschema);
module.exports=Student;
