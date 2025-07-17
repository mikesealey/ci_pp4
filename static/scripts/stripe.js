const stripe = Stripe(window.stripe_public_key);
const elements = stripe.elements();
const card = elements.create("card", {
  hidePostalCode: true
});
card.mount("#card-element");

const form = document.getElementById("payment-form");
const submitButton = document.getElementById("submit-button");



form.addEventListener("submit", async (e) => {
    e.preventDefault();
    submitButton.disabled = true;

    const res = await fetch(window.payment_intent_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": window.csrf_token
      },
      body: JSON.stringify({
        name: document.getElementById("name-on-card").value
      })
    });

    const { client_secret } = await res.json();

    const result = await stripe.confirmCardPayment(client_secret, {
      payment_method: {
        card,
        billing_details: {
          name: document.getElementById("name-on-card").value,
          address: {
            postal_code: document.getElementById("bill-postcode").value
          }
        }
      }
    });

    if (result.error) {
      document.getElementById("card-errors").textContent = result.error.message;
      submitButton.disabled = false;
    } else if (result.paymentIntent && result.paymentIntent.status === 'succeeded') {
      window.location.href = "/basket/success/";
    }
});
