$(document).ready(function() {
  $('#fullpage').fullpage({
    //Navigation
    anchors: [],
    navigation: false,
    fitToSection: true,

    //Scrolling
    scrollBar: true,
    css3: true,

    //Accessibility
    keyboardScrolling: true,

    //Design
    resize: true,
    paddingTop: '18em',
    verticalCentered: true,
    responsiveWidth: 1100
  });
});