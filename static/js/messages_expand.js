var main = function(){
    $('.article').click(function(){
        $('.article').removeClass('current');
        $('.description').hide();
        
        $(this).addClass('current');
        $(this).children('.description').show();
        
        });

  
$(document).ready(main);
