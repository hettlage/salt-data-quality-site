(function($) {
    $(document).ready(function() {
        $('.datepicker').datepicker({
            dateFormat: 'yy-mm-dd'
                                    });
    });
})(jQuery);

$(document).ready(function(){
  $('.dropdown-submenu a.submenu').on("click", function(e){
    $(this).next('ul').toggle();
    e.stopPropagation();
    e.preventDefault();
  });
});

