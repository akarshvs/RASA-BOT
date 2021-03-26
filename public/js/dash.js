$(document).ready(function(){

  function myfunction(sitem, sitemul){
  $(sitem).click(function(){
      $(sitemul).fadeToggle();
    });
  }


  $('.profile img').click(function(){
    $('.profile-data').fadeToggle();
  });


myfunction('.s-item3','.s-item3 ul');

$('.statictr').click(function(){
$(this).find('td:first').text();
$(this).next().toggle();
});


$('.update').click(function(){
  var id = $(this).closest("tr")   // Finds the closest row <tr>
                       .find("#sid")    // Gets a descendent with class="nr"
                       .val();

  var name = $(this).closest("tr")   // Finds the closest row <tr>
    .find("#sname")    // Gets a descendent with class="nr"
    .val();
    var position = $(this).closest("tr")   // Finds the closest row <tr>
      .find("#spos")    // Gets a descendent with class="nr"
      .val();
      var department = $(this).closest("tr")   // Finds the closest row <tr>
        .find("#sdep")    // Gets a descendent with class="nr"
        .val();
        var contact = $(this).closest("tr")   // Finds the closest row <tr>
          .find("#scon")    // Gets a descendent with class="nr"
          .val();

  $.post('/dashboard/employee/insert',
  {
   id: id,
   name:name,
   position:position,
   department:department,
   contact:contact
  },
  function(data,status){
   alert("updated");
   location.reload();
  });
}) ;


$('.supdate').click(function(){
  var sid = $(this).closest("tr")   // Finds the closest row <tr>
                       .find("#stid")    // Gets a descendent with class="nr"
                       .val();
  var admissionno = $(this).closest("tr")   // Finds the closest row <tr>
                       .find("#admn")    // Gets a descendent with class="nr"
                       .val();

  var name = $(this).closest("tr")   // Finds the closest row <tr>
    .find("#stname")    // Gets a descendent with class="nr"
    .val();
    var department = $(this).closest("tr")   // Finds the closest row <tr>
      .find("#stdep")    // Gets a descendent with class="nr"
      .val();
      var department_type = $(this).closest("tr")   // Finds the closest row <tr>
        .find("#stdept")    // Gets a descendent with class="nr"
        .val();
        var semester = $(this).closest("tr")   // Finds the closest row <tr>
          .find("#ssem")    // Gets a descendent with class="nr"
          .val();

  $.post('/dashboard/student/update',
  {
   id: sid,
   admission_no: admissionno,
   name:name,
   department:department,
   department_type:department_type,
   semester:semester
  },
  function(data,status){
   alert("updated");
   location.reload();
  });
}) ;
$('.feesup').click(function(){
  var famount=$(this).closest('tr').find('.feein').val();
  var fid=$(this).closest('tr').find('.feeid').text();
  $.post('/dashboard/fees/update',
  {
   id:fid,
   amount: famount
  },
  function(data,status){
   alert(status);
   location.reload();
  });
}) ;
$('#fineup').click(function(){
   console.log("clicked");
  $.post('/dashboard/fine/update',
  {
   id: $('#fineid').text(),
   famount: $('#famount').val(),
   ldate: $('#lastd').val(),
   sfdate:$('#sfdate').val(),
   sfamount:$('#sfamount').val(),

  },
  function(data,status){
   alert("Fine updated");

   location.reload();
  });
}) ;

$(".addstudent").click(function(){
  $(".addForm").fadeToggle();
});
$(".addC").click(function(){
  $(".addForm").fadeToggle();
});
$('.del').click(function(){
  var cid=$(this).closest('div').find('.cid').text();
  $.post('/dashboard/complaint/delete',
  {
   id: cid

  },
  function(data,status){
   alert("complaint deleted");

   location.reload();
  });
});
});
