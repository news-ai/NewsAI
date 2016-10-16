window.Intercom("boot", {
  app_id: "ur8dbk9e"
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

function changePricingClass() {
    if (document.getElementById("pricingClass").className === "annually") {
        // Change label color & the button
        document.getElementById("pricingClass").className = "monthly";
        document.getElementById("monthlyLabel").className = "active";
        document.getElementById("annuallyLabel").className = "";

        // Update prices
        document.getElementById("personalPrice").innerHTML = "9.99";
        document.getElementById("businessPrice").innerHTML = "49.99";
        document.getElementById("ultimatePrice").innerHTML = "79.99";
    } else {
        // Change label color & the button
        document.getElementById("pricingClass").className = "annually";
        document.getElementById("monthlyLabel").className = "";
        document.getElementById("annuallyLabel").className = "active";

        // Update prices
        document.getElementById("personalPrice").innerHTML = "7.99";
        document.getElementById("businessPrice").innerHTML = "39.99";
        document.getElementById("ultimatePrice").innerHTML = "63.99";
    }
}