var mongoose = require('mongoose');
var Schema      = mongoose.Schema;
var Userschema = new Schema({
  username:String,
  password:String,
  email:String
},
{
  collection:'login'
});
User = mongoose.model('User',Userschema);
module.exports=User;
module.exports.getUserByUsername =function(username,callback){
  var query ={username:username};
  User.findOne(query,callback);
}
module.exports.getUserById =function(id,callback){
  User.findById(id,callback);
}
module.exports.comparePass = function(password,pass,callback){
  if(password==pass){
    return callback(null,true);
  }
  else
  {
    return callback(null,false);
  }


}
