$(document).ready(function(){
   $(".comment-reply-btn").click(function(event){
         event.preventDefault();
         $(this).parent().next(".comment-reply").fadeToggle();
   })

})




