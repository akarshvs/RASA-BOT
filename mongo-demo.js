var express = require('express');
var path= require('path');
var mongoose = require('mongoose');
var bodyParser = require('body-parser');
var hbs=require('express-handlebars');
var cookieParser=require('cookie-parser');
var session = require('express-session');
var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;
var User= require('./models/user');
var Staff = require('./models/staff');
var Student = require('./models/student');
var Payment = require('./models/payment');
var Fees = require('./models/fees');
var Fine = require('./models/fine');
var Complaint  = require('./models/complaint');
mongoose.connect('mongodb://localhost:27017/cmsbot',{ useNewUrlParser: true });
var db= mongoose.connection;
var app = express();
app.engine('hbs',hbs({extname: 'hbs' ,defaultLayout:'layout', layoutsDir: __dirname+'/views/layout'}));
app.set('views',path.join(__dirname,'views'));
app.set('view engine','hbs');
app.use(express.static(__dirname + '/public'));
app.use(express.json());
app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());
app.use(cookieParser());

app.use(session({
  secret: 'secret',
  saveUninitialised:true,
  resave:true
}));
app.use(passport.initialize());
app.use(passport.session());


passport.use(new LocalStrategy( function(username,password,done){
User.getUserByUsername(username,function(err,user){
  if(err) throw err;
  if(!user){
    return(null,false,{message:'unknown user'});

  }
 User.comparePass(password,user.password,function(err,isMatch){
   if(err) throw err;
   if(isMatch){
     console.log("login success!!");

     return done(null,user);
   }
   else{

     console.log("invalid password");
     return done(null,false,{message:"failed to login"});
   }
 });
});
}));
passport.serializeUser(function(user,done){
  done(null,user.id);
});
passport.deserializeUser(function(id,done){
  User.getUserById(id,function(err,user){
    done(err,user);
  });
});
app.get('/dashboard',ensureAthenticated,function(req,res){

res.render('employee');

});
app.get('/login',function(req,res){

    res.sendFile(__dirname+'/adminindex.html');

});
app.get('/',function(req,res){

    res.sendFile(__dirname+'/index.html');

});
app.get('/dashboard/employee',ensureAthenticated,function(req,res,next){
Staff.find({},function(err,staff){
  res.render('employee',{data: staff});
});

});
app.post('/dashboard/employee/insert',ensureAthenticated,function(req,res,next){
var item =
{

  name: req.body.name,
  position: req.body.position,
  department: req.body.department,
  contact: req.body.contact
};

var   id= req.body.id;
Staff.findById(id,function(err,doc){
  if(err){
    console.log("not found");
  }
  else{
      doc.name= req.body.name,
      doc.position=req.body.position,
      doc.department= req.body.department,
      doc.contact= req.body.contact
      doc.save();

  }

});
res.redirect('/dashboard/employee');
});
app.get('/dashboard/student',ensureAthenticated,function(req,res,next){
Student.find({},function(err,student){
  res.render('student',{data: student});
});

});
app.post('/dashboard/student/insert',ensureAthenticated,function(req,res,next){
  var item =
  {
    admission_no: req.body.admission_no,
    name: req.body.name,
    department: req.body.department,
    department_type: req.body.department_type,
    graduate:req.body.graduate,
    semester: req.body.semester
  };
  var std= new Student(item);
  std.save();
  res.redirect('/dashboard/student');

});
app.post('/dashboard/student/update',ensureAthenticated,function(req,res,next){
  var item =
  {
    admission_no: req.body.admission_no,
    name: req.body.name,
    department: req.body.department,
    department_type: req.body.department_type,
    semester: req.body.semester
  };
  var id = req.body.id;
  Student.findById(id,function(err,doc){
    if(err){
      console.log("not found");
    }
    else{
        doc.admission_no= req.body.admission_no,
        doc.name= req.body.name,
        doc.department=req.body.department,
        doc.department_type= req.body.department_type,
        doc.semester= req.body.semester
        doc.save();
       console.log("saved student");
    }

  });
  res.redirect('/dashboard/student');
});
app.get('/dashboard/fine',ensureAthenticated,function(req,res,next){
  Fine.find({},function(err,fine){
    res.render('payfine',{data:fine});
  });;
});
app.post('/dashboard/fine/update',ensureAthenticated,function(req,res,next){
  Fine.findById(req.body.id,function(err,doc){
   doc.last_date =req.body.ldate,
   doc.fine =req.body.famount,
   doc.superfine=req.body.sfamount,
   doc.superfine_date=req.body.sfdate,
   doc.save();
  });
  res.redirect('/dashboard/fine');
});
app.get('/dashboard/fees',ensureAthenticated,function(req,res,next){
  Fees.find({},function(err,fees){
    res.render('fees',{data:fees});
  });
});
app.post('/dashboard/fees/update',ensureAthenticated,function(req,res,next){
  Fees.findById(req.body.id,function(err,doc){
  if(!err){
    doc.fees_amount=req.body.amount,
    doc.save();
    console.log("svaaa");
  }
  else{
    console.log("not found");
  }
  });
  res.redirect('/dashboard/fees');
});
app.get('/dashboard/payment',ensureAthenticated,function(req,res,next){
  Payment.find({},function(err,payment){
    res.render('payments',{data:payment});
  });

});
app.get('/dashboard/complaint',ensureAthenticated,function(req,res,next){
  Complaint.find({},function(err,doc){
    res.render('complaints',{data:doc});
  });

});
app.post('/dashboard/complaint/delete',ensureAthenticated,function(req,res,next){
  var  cid=req.body.id;
  Complaint.findByIdAndRemove(cid,function(err,doc){
    res.render('complaints',{data:doc});
  });

});
app.get('/verify',function(req,res){
  console.log(req.query.payment_status);
  if(req.query.payment_status=="Credit")
  {
    Payment.findOne({"req_id": req.query.payment_request_id}, function (err, payment) {
      if(!err){
        payment.validatefees ="true";
        payment.save();
      }else
      {
        console.log("not found");
      }


    });

  }
  else
  {
    res.send("payment UnSuccess");
  }
});
app.post('/login',
  passport.authenticate('local' ,{ successRedirect: '/dashboard',
                                   failureRedirect: '/login' }),
  function(req, res) {
    // If this function gets called, authentication was successful.
    // `req.user` contains the authenticated user.
res.render('employee',{data: Staff});
  });

  app.get('/logout',function(req,res){
    req.logout();
    res.redirect('/login');
  });
function ensureAthenticated(req,res,next){
  if(req.isAuthenticated()){
    return next();
  }
  else{
    res.redirect("/login");
  }
}
app.listen(3000)
