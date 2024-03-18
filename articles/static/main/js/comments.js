$(document).ready(function(){
   $(".comment-reply-btn").click(function(event){
         event.preventDefault();
         $(this).parent().next(".comment-reply").fadeToggle();
   })

   $(".reply-form-btn").click(function(event){
         event.preventDefault();
         $(this).parent().next(".reply-form").fadeToggle();
   })

})




