function increaseQtyField(field){
    if (Number($("#qty-field-" + field).val()) < Number($("#qty-in-stock-" + field).text())){
      $("#qty-field-" + field).val(Number($("#qty-field-" + field).val()) +1)
      $("#update-prompt-" + field).text("UPDATE")
    }
}

function decreaseQtyField(field){
    if (Number($("#qty-field-" + field).val()) > 1) {
      $("#qty-field-" + field).val(Number($("#qty-field-" + field).val()) -1)
      $("#update-prompt-" + field).text("UPDATE")
    }
}

function updateOrderQty(field) {
    const updateUrl = document.getElementById("update-url").value
    const newQty = Number($("#qty-field-" + field).val())

    fetch(updateUrl, {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify({
        item_id: field,
        qty: newQty
        })
    })
    .then(res => {
        if (!res.ok) {
        console.log("Could not update quantity") // handle more gracefully/show a toast?
        return
        }
        return res.json()
    })
    .then(data => {
        if (!data) return
        $("#basket-total").text("£" + data.basket_total)
        $("#order-total").text("£" + data.order_total)
        $("#update-prompt-" + field).text("")
    })
}