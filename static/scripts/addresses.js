$(document).ready(function () {
    console.log("Addresses!");

    $("#copy-billing-address").on("click", function (e) {
        e.preventDefault();

        const billAddress = {
            name: $("#name-on-card").val(),
            address1: $("#bill-address-line-1").val(),
            address2: $("#bill-address-line-2").val(),
            townCity: $("#bill-address-town-city").val(),
            postCode: $("#bill-postcode").val(),
        };
        $("#ship-name").val(billAddress.name);
        $("#ship-address-line-1").val(billAddress.address1);
        $("#ship-address-line-2").val(billAddress.address2);
        $("#ship-town-city").val(billAddress.townCity);
        $("#ship-postcode").val(billAddress.postCode);
        
    });

   
});