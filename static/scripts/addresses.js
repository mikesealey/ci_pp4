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
        $("#ship-address-town-city").val(billAddress.townCity);
        $("#ship-postcode").val(billAddress.postCode);
        
    });

    $("#bill-address-selector").on("change", function () {
    const selected = $(this).find(":selected");

    if (!selected.val()) return;
    $("#bill-name").val(selected.data("name"));
    $("#bill-address-line-1").val(selected.data("address1"));
    $("#bill-address-line-2").val(selected.data("address2"));
    $("#bill-address-town-city").val(selected.data("townCity"));
    $("#bill-postcode").val(selected.data("postcode"));
});

   $("#ship-address-selector").on("change", function () {
    const selected = $(this).find(":selected");

    if (!selected.val()) return;

    $("#ship-name").val(selected.data("name"));
    $("#ship-address-line-1").val(selected.data("address1"));
    $("#ship-address-line-2").val(selected.data("address2"));
    $("#ship-address-town-city").val(selected.data("townCity"));
    $("#ship-postcode").val(selected.data("postcode"));
});
});