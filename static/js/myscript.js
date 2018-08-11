$(function() {
  $(window).scroll(function() {
        var winTop = $(window).scrollTop();
    if (winTop >= 20) {
            $("header").addClass("sticky-header");
    } else {
            $("header").removeClass("sticky-header");
    }
  })
})


$(function(){
  var btnSubmit = $('#share');
  btnSubmit.attr('disabled', 'disabled');
  $('input[name=chosen]').change(function(e){
    if($(this).val() == 'agree'){
      btnSubmit.removeAttr('disabled');

    }else{
      btnSubmit.attr('disabled', 'disabled');

    }

  });

});
