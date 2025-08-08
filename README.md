# The Woodshed

This project is an E-Commerce site for selling artisanal woodworking projects, such as chairs, tables, and bowls, as part of my Level 5 Diploma in Web Application Development.

This project is for educational purposes only. Do not attempt to place an order with real payment details. No purchases will be fulfilled.

## Contents

- [The Woodshed](#the-woodshed)
  - [Contents](#contents)
  - [User Stories](#user-stories)
    - [As a user](#as-a-user)
  - [Design Considerations](#design-considerations)
    - [Creating a wireframe](#creating-a-wireframe)
  - [Code Sources](#code-sources)
  - [Features](#features)
  - [Lighthouse Reports and Validation](#lighthouse-reports-and-validation)
    - [Performance](#performance)
    - [Accessibility](#accessibility)
    - [Code Validation](#code-validation)
    - [Code Documentation](#code-documentation)
  - [Testing](#testing)
    - [Testing User Stories](#testing-user-stories)
    - [Additional Testing](#additional-testing)
    - [Functional Testing](#functional-testing)
    - [Unit Tests in Django](#unit-tests-in-django)
    - [Browser Compatibility](#browser-compatibility)
  - [Deployment](#deployment)
  - [Cloning This Repo](#cloning-this-repo)
  - [Forking This Repo](#forking-this-repo)
  - [Credits](#credits)
    - [Photos](#photos)
    - [Image Generation](#image-generation)
  - [Future Developments](#future-developments)
    - [Back office or Admin Panels](#back-office-or-admin-panels)

---

## The Woodshed

## Contents

## User Stories

### As a user

## Design Considerations

### Creating a wireframe

## Code Sources

## Features

## Lighthouse Reports and Validation

### Performance

### Accessibility

### Code Validation

### Code Documentation

## Testing

### Testing User Stories

### Additional Testing

### Functional Testing

### Unit Tests in Django

### Browser Compatibility

## Deployment

## Cloning This Repo

## Forking This Repo

## Credits

### Site Photos
Background Image: https://www.pexels.com/photo/focused-artisan-making-hole-on-plank-with-hammer-and-chisel-5974283/

Icon Image: https://iconduck.com/icons/157332/hammer

### Product Images

Initially, I had hoped to find more images on sites like pexls, but it proved harder than expected to find images where the woodwork was the subject of the photo, and there were multiple angles of the woodwork. My mentor suggested using AI to generate the images, though this became problematic when, frequently, the image generator would never quite be able to show the _same item_ each time. There would frequently be differences in the product between each image, so much that it looked like a slightly different product.

This meant that I had to use my own, real-life photos of my own, real-life creations, despite being a very inexperienced woodworker, and an even less experienced photographer.

|Product | Source | Image URLs | 
|--------|--------|-------|
| Small Pine Vase| Mike Sealey| http://res.cloudinary.com/dvomhvuag/image/upload/v1754077575/jfo4rcxylzwtjn4gwkwx.jpg | |
|Live Edge Coffee Table| Mike Sealey| http://res.cloudinary.com/dvomhvuag/image/upload/v1753907033/jq0bdlagqwgpytxgsfw7.jpg, http://res.cloudinary.com/dvomhvuag/image/upload/v1753907036/roevnwpt6vnhsfxx9e6p.jpg, http://res.cloudinary.com/dvomhvuag/image/upload/v1753907038/lxjp0hxxkzfuixpmgwz2.jpg, http://res.cloudinary.com/dvomhvuag/image/upload/v1753907040/anhd29bojr6kpoyv3tmw.jpg, http://res.cloudinary.com/dvomhvuag/image/upload/v1753907043/qrsl46nhvp4jeaz8sohe.jpg, http://res.cloudinary.com/dvomhvuag/image/upload/v1753907046/l66ufnbgj50cgyk06man.jpg, http://res.cloudinary.com/dvomhvuag/image/upload/v1753907048/jovs97qcboexlpmkqjfa.jpg  |
|Large Wooden Vase | ChatGPT | http://res.cloudinary.com/dvomhvuag/image/upload/v1754077417/zanplloxfvt2zjqihezj.png http://res.cloudinary.com/dvomhvuag/image/upload/v1754077415/tsffoquw42r3ccwca41b.png http://res.cloudinary.com/dvomhvuag/image/upload/v1754077418/prdmphsxyfrrfgywgscl.png|
|White Oak Pestle & Mortar| Mike Sealey | http://res.cloudinary.com/dvomhvuag/image/upload/v1754077789/s7zk3duny5j0of2qme4e.jpg http://res.cloudinary.com/dvomhvuag/image/upload/v1754077791/qxfces1y78h5fgwg7fbf.jpg http://res.cloudinary.com/dvomhvuag/image/upload/v1754077792/zka8vxxpzqnhimoivv4r.jpg http://res.cloudinary.com/dvomhvuag/image/upload/v1754077794/hd2nnn8q6xhwrfmnk0ey.jpg http://res.cloudinary.com/dvomhvuag/image/upload/v1754077796/advtm4blwthl3sia2lf6.jpg |
|Live edge Incense Burner | Mike Sealey | http://res.cloudinary.com/dvomhvuag/image/upload/v1754078129/lopmmwxxy08hpe7eb93e.jpg http://res.cloudinary.com/dvomhvuag/image/upload/v1754078127/udtkleu6jg8k8lkixmxx.jpg http://res.cloudinary.com/dvomhvuag/image/upload/v1754078131/ee04p3u4venrm4vnrwzg.jpg |
|6" Bowl | Mike Sealey | http://res.cloudinary.com/dvomhvuag/image/upload/v1753908669/p5zkaamkyaib8wht2ioi.jpg http://res.cloudinary.com/dvomhvuag/image/upload/v1753908672/b4ubtdsufsdt9axyqztn.jpg http://res.cloudinary.com/dvomhvuag/image/upload/v1753908674/bde0rng9llngfy2rft5f.jpg |
|Openback Oak Dining Chair| ChatGPT | http://res.cloudinary.com/dvomhvuag/image/upload/v1754080088/dph34btg67ktcuwzkuis.png |
|Spindleback Pine Chair | ChatGPT| http://res.cloudinary.com/dvomhvuag/image/upload/v1754079825/hzdzvaeceru8ghv28djw.png |


## Future Developments

### Back office or Admin Panels
    
    






<!-- 
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

Django management commands tutorial here: https://www.geeksforgeeks.org/python/custom-django-management-commands/  -->