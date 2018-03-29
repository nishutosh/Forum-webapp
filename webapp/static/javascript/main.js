$(document).ready(
	

	function(){
    if($(window).width()<445){
$("#submitsearch").attr("src",'/static/images/searchb.png');}




    if($(window).width()>445){
    $("#submitsearch").hover(function(){
         $("#id_searchinfo").fadeIn("fast",
     	     function(){
                 $("#search").mouseleave(
       	                  function(){
								     $("#id_searchinfo").fadeOut(100);
								     $("#submitsearch").attr("src",'/static/images/search.png');
                                    });
                  });
            $("#submitsearch").attr("src",'/static/images/searchb.png');
           
           });}
          $("#id_profilepic").change(
      	  function(){
          $("#submit_pic").removeAttr("disabled");});
          $("#nav").slideDown("slow",function(){

           $("#nav").delay(6000).slideUp("slow");

          });	
          $(".ah").hover(function(){

          	$(this).css("color","orange")
          },function(){$(this).css("color","white");});
          




});



