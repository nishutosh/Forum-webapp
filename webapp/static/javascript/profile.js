$(document).ready(function(){
  if($(window).width()<445){
$("#hide").css("display","block");
$("#mp").css("display","none");
}
   
   $("#navi").hover(function(){

      $(".mplist").slideDown("fast");
    },function(){
     $("#menubox").mouseleave(function(){
      $(".mplist").slideUp("fast");
    } );   
    });



  
    $("#mp").hover(function(){

      $(".mplist").slideDown("fast");
      $("#mp").css("color","grey");
    },function(){
     $("#menubox").mouseleave(function(){
      $(".mplist").slideUp("fast");
      $("#mp").css("color","white");
    } );   
    });
 
    $("#mo").hover(function(){

      $(".mplist1").slideDown("fast");
      $("#mo").css("color","grey");
    },function(){
     $("#menubox1").mouseleave(function(){
      $(".mplist1").slideUp("fast");
      $("#mo").css("color","white");
    } );
    });
    
    $(".messages").fadeIn("slow",function(){

      
     $(".messages").delay(1000).fadeOut("slow");

    });
    $(".delq").click(function(event){

      var r=confirm("Do you want to delete this question");
      if(r==false){
          event.preventDefault();

      }
    });
    $(".dela").click(function(event){

      var r=confirm("Do you want to delete this answer");
      if(r==false){
          event.preventDefault();

      }
    });
    $("#changedel").click(function(event){

      var r=confirm("Are you sure you want to delete the profile?");
      if(r==false){
          event.preventDefault();

      }
    });
    $("#quesclick").click(function(){

    $("#quesclick").css("color","black");
    $("#quesclick").css("background-color","white");
    $("#anshide").css("display","none");
    $("#queshide").css("display","block");

    })
    $("#ansclick").click(function(){

    $("#queshide").css("display","none");
    $("#anshide").css("display","block");
    });

	});
$(window).resize(function(){

  if ($(window).width() > 445) {
     $('#hide').css("display","none");
     $("#mp").css("display","block");
    }
  else{
   $("#hide").css("display","block");
    $("#mp").css("display","none");

    }


});


    