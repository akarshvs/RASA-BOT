(document).ready(function(){
  function myfunction(sitem, sitemul){
    $(sitem).click(function(){
      $(sitemul).fadeToggle();
    });
  }
  $('.profile img').click(function(){
    $('.profile-data').fadeToggle();
  });

myfunction('.s-item1','.s-item1 ul');
myfunction('.s-item2','.s-item2 ul');
myfunction('.s-item3','.s-item3 ul');
});
