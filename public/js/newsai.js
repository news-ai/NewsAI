window.Intercom("boot", {
  app_id: "ur8dbk9e"
});

function openModal(){
    todayDateString = new Date().toJSON().slice(0, 10)
    vex.dialog.open({
        message: 'Fill out the form below, and someone on the NewsAI team will get in touch with you very soon!',
        input: [
            '<style>',
                '.vex-custom-field-wrapper {',
                    'margin: 1em 0;',
                '}',
                '.vex-custom-field-wrapper > label {',
                    'display: inline-block;',
                    'margin-bottom: .2em;',
                '}',
            '</style>',
            '<form action="http://email3.newsai.co/t/d/s/pbjhr/" method="post" id="subForm">',
                '<p>',
                    '<label for="fieldName">Name</label><br />',
                    '<input id="fieldName" name="cm-name" type="text" />',
                '</p>',
                '<p>',
                    '<label for="fieldEmail">Email</label><br />',
                    '<input id="fieldEmail" name="cm-pbjhr-pbjhr" type="email" required />',
                '</p>',
                '<p>',
                    '<button type="submit" class="vex-dialog-button-primary vex-dialog-button vex-first">Request demo</button>',
                '</p>',
            '</form>'
        ].join(''),
        buttons: [],
        callback: function (data) {
            if (!data) {
                return console.log('Cancelled');
            }
        }
    })

}

function changePricingClass() {
    if (document.getElementById("pricingClass").className === "annually") {
        // Change label color & the button
        document.getElementById("pricingClass").className = "monthly";
        document.getElementById("monthlyLabel").className = "active";
        document.getElementById("annuallyLabel").className = "";

        // Update prices
        document.getElementById("personalPrice").innerHTML = "9.99";
        document.getElementById("businessPrice").innerHTML = "35.99";
        document.getElementById("ultimatePrice").innerHTML = "54.99";
    } else {
        // Change label color & the button
        document.getElementById("pricingClass").className = "annually";
        document.getElementById("monthlyLabel").className = "";
        document.getElementById("annuallyLabel").className = "active";

        // Update prices
        document.getElementById("personalPrice").innerHTML = "7.99";
        document.getElementById("businessPrice").innerHTML = "29.99";
        document.getElementById("ultimatePrice").innerHTML = "43.99";
    }
}
