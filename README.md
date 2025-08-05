# ci_pp4


Background Image: https://www.pexels.com/photo/focused-artisan-making-hole-on-plank-with-hammer-and-chisel-5974283/

Icon Image: https://iconduck.com/icons/157332/hammer

Useful SO on washing out the peripherary images in the gallery: https://stackoverflow.com/questions/74641294/how-to-wash-out-colors-with-css-filters

Stripe "International" cards (ie using those with UK Postcodes instead of US ZipCodes)https://docs.stripe.com/testing#international-cards


Fun problem to encounter: If someone orders more than I have in stock the constraint saying stock level must be greater than 0 throws an error. This needs some front-end protections.
Demonstration: https://jam.dev/c/d803a524-1b8e-4a17-a5db-3fafcd342194
```
Request Method:	GET
Request URL:	http://127.0.0.1:8000/basket/success/
Django Version:	4.2.19
Exception Type:	IntegrityError
Exception Value:	
CHECK constraint failed: qty_in_stock
```
Resolution: 
https://jam.dev/c/8a0d7b9e-1154-418f-b3ee-3a0415ae8334

``` Python
if not created:
        # Must check if enough stock _exists_ to add to basket
        new_qty = item.qty + 1
        if new_qty > product.qty_in_stock:
            # If not enough stock, don't update the quantity
            messages.error(
                request,
                f"Cannot add another {product.name} — only {product.qty_in_stock} in stock."
            )
        else:
            # else update the quantity and save the item
            item.qty = new_qty
            item.save()
            message = f"Added {product.name} to basket"
            messages.success(request, message)
```

This check starts with "is this item already in the basket, or have we created an entry in the basket for it?" - If not created, then it already exists, and we simply want to increase the quantity, _but_ we must check that there's stock to do so. We add one to the ammount of stock in the basket, and compare it to the ammount in stock. We'll let the customer know if they're trying to add more to their basket than we have in stock.

This check only occurs when there is already one in the basket. Prior to the item being added to the basket for the first time, the "Add to basket" button is disabled of `product.qty_in_stock` is zero.

Multi-field search with Q
https://www.freecodecamp.org/news/what-is-q-in-django-and-why-its-super-useful
Lets me use the seach bar to search name and/or material and/or finish

NetNinja Django Testing tutorial - https://www.youtube.com/watch?v=OfiCALrGE14&list=PL4cUxeGkcC9ic9O6xDW2d1qMp3rMOb0Nu

Django management commands tutorial here: https://www.geeksforgeeks.org/python/custom-django-management-commands/ 