jQuery(function($) {
    $('#download-button').localScroll({
        duration: 1000
    });
});

function alturaMaxima() {
    var altura = $(window).height();
    $(".full-screen").css('min-height', altura);
}

$(document).ready(function() {
    alturaMaxima();
    $(window).bind('resize', alturaMaxima);
});

if (navigator.userAgent.match(/IEMobile\/10\.0/)) {
    var msViewportStyle = document.createElement('style')
    msViewportStyle.appendChild(
        document.createTextNode(
            '@-ms-viewport{width:auto!important}'
        )
    )
    document.querySelector('head').appendChild(msViewportStyle)
}