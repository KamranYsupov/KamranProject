$(document).ready(function(){
   $(".message-menu-btn").click(function(event){
         event.preventDefault();
         $(this).parent().next(".message-menu").fadeToggle();
   })

   $(".change_message_btn").click(function(event){
         event.preventDefault();
         $(this).parent().next(".change_message_form").fadeToggle();
   })

})

