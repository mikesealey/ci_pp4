const stripe = Stripe(window.stripe_public_key);
const elements = stripe.elements();
const card = elements.create("card", {
  hidePostalCode: true
});
card.mount("#card-element");

const $form = $("#payment-form");
const $submitButton = $("#submit-button");



$form.on("submit", async function (e) {
  e.preventDefault();
  $submitButton.prop("disabled", true);

  const res = await fetch(window.payment_intent_url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": window.csrf_token
    },
    body: JSON.stringify({
      name: $("#name-on-card").val(),
      shipping: {
        name: $("#ship-name").val(),
        address1: $("#ship-address-line-1").val(),
        address2: $("#ship-address-line-2").val(),
        town_city: $("#ship-town-city").val(),
        postcode: $("#ship-postcode").val(),
        phone: $("#ship-phone").val() || "",
        email: $("#email").val() || ""
      }
    })
  });

  const { client_secret } = await res.json();

  const result = await stripe.confirmCardPayment(client_secret, {
    payment_method: {
      card: card,
      billing_details: {
        name: $("#name-on-card").val(),
        address: {
          postal_code: $("#bill-postcode").val()
        }
      }
    }
  });

  if (result.error) {
    $("#card-errors").text(result.error.message);
    $submitButton.prop("disabled", false);
  } else if (result.paymentIntent && result.paymentIntent.status === "succeeded") {
    console.log("SUCCESS!")
    window.location.href = "/basket/success/";
  }
});
