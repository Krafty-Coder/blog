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
