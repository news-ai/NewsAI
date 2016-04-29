$(document).ready(function() {
  $('#fullpage').fullpage({
    //Navigation
    anchors: [],
    navigation: false,
    fitToSection: false,

    //Scrolling
    scrollBar: true,
    css3: true,

    //Accessibility
    keyboardScrolling: true,

    //Design
    resize: false,
    paddingTop: '18em',
    verticalCentered: true,
    responsiveWidth: 1000
  });
});