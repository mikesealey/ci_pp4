const stripe = Stripe("{{ stripe_public_key }}");
const elements = stripe.elements();
const card = elements.create("card");
card.mount("#card-element");

const form = document.getElementById("payment-form");
const submitButton = document.getElementById("submit-button");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    submitButton.disabled = true;

    const res = await fetch("{% url 'create_payment_intent' %}", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": "{{ csrf_token }}"
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
          name: document.getElementById("name-on-card").value
        }
      }
    });

    if (result.error) {
      document.getElementById("card-errors").textContent = result.error.message;
      submitButton.disabled = false;
    } else {
      if (result.paymentIntent.status === 'succeeded') {
        form.submit();
      }
    }
});