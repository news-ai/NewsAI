function getHeight() {
  // return document.getElementById('firstDiv').clientHeight;
  return window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
}
function getWidth() {
  return window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
}
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
    responsiveWidth: 1100
  });
});