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


## User Stories
For this project I have made use of a simple Kanban Board, which is now available as a feature of Github Projects - You can see it here: https://github.com/users/mikesealey/projects/3 

### As a user
    - I want to easily log in/out So that to keep my details and orders safe at minimal inconvenience.
    - I want view more specific details about a product So that I can make an informed decision about price, material, finish, etc
    - I want to see a gallery/carousel of images depicting a particular product So that I can see physical details not covered by basic stats.
    - I want to be able to view a list of products So that I can select some products to purchase.
    - I want to be able to see products in a specific category So that I can more easily find products to fit my requirements
    - I want to be able to add products to my wishlist So that I can save for later.
    - I want to be able to add products from wishlist to basket, So that I can keep track of products that I like and buy them
    - I want to see my basket total So that I can avoid going over-budget.
    - I want to be able to recover my account/password So that I don't lose my account/order history/wishlist items.
    - I want To easily register for an account So that I can save account/address details or past orders
    - I want recive an email confirming successful sign-up So that I know other email confirmations wont go directly to junk.

## Design Considerations

Early on in the development of The Woodshed, I knew that I would like to make reusable components as much as possible. The Product Card shown in the wireframe is itself an HTML template. 

![Reusable Components - The Product Card](./readme_images/Screenshot%202025-08-09%20at%2016.06.50.png  "Showing the reusable Product Card component")

This means that when passing an array of products, I can simply loop over them and pass in a _this-product_ to a Product Card as follows
```Django
{% for product in products %}
    <div class="col-12 col-sm-6 col-lg-4 px-5 pb-4">
        {% include "components/product_card.html" with product=product in_wishlist=False %}
    </div>
{% endfor %}
```
This means that I can work on _one product card_ and have the changes reflect everywhere the products are listed (Basket, Wishlist, all products, filtered products).

Later in the development of this project, through a discussion with my mentor, I found that I had to tackle some interesting design-decisions around how stock is handled, particularly at the batch/one-off end of the e-commerce scale.

The items being sold are frequently one of one, or one of only a handful of items made and listed for sale. Naturally, there are protections against adding an out-of-stock item to basket, but it's possible that two people could add the same one-of-a-kind item to their basket before either has checked out. They could then both proceed to checkout, and one customer could end up sorely disapointed.

I explored a few ways of handling this in order to try to strike a balance between making the sale and not giving a customer a bad experience. In the end, I opted to decrement the stock level when a user adds the item to their basket, but have an expiry on the item so that abandonned baskets don't tie up the stock.

When an item is added to the basket, a timestamp is also saved. In `settings.py`, the variable `BASKET_RESERVATION_HOURS = 3` is used in conjunction with `added_to_basket_at` from `basket/models.py` to determine at what point an item has been abandonned in the basket. Heroku Scheduler will then run a job created in `/basket/management/commands/expire_basket_items.py` which replenishes the stock, removes it from the user's basket and places it into the user's wishlist instead.

A lot of the initial understanding of management commands came from this Geeks4Geeks tutorial https://www.geeksforgeeks.org/python/custom-django-management-commands/ 

### Creating a wireframe

I used Balsamiq Wireframes to mock up a plan for how I would like The Woodshed to look.

![Homepage Wireframe](./readme_images/Screenshot%202025-08-09%20at%2015.54.09.png "An initial design of the Homepage in Balsamiq Wireframes")

## Code Sources
- Django management commands tutorial here: https://www.geeksforgeeks.org/python/custom-django-management-commands/ (Used for scheduling expir)

- Multi-field search with Q
https://www.freecodecamp.org/news/what-is-q-in-django-and-why-its-super-useful
Lets me use the seach bar to search name and/or material and/or finish

- NetNinja Django Testing tutorial - https://www.youtube.com/watch?v=OfiCALrGE14&list=PL4cUxeGkcC9ic9O6xDW2d1qMp3rMOb0Nu

## Other Contributions
All of the product descriptions were generated by giving a simple prompt to ChatGPT like: 
>  "Please help write a product description of a coffee table I made. I want a couple of paragraphs, no bullet points, just a nice description. Perhaps 250 words. A live-edge coffee table, planed from a cross section of a sycamore trunk at the point of bifurcation"

Which returned:

> This handcrafted live-edge coffee table is a striking fusion of natural beauty and artisan craftsmanship. Created from a cross section of a sycamore trunk, it captures a rare moment in the tree’s growth—where the trunk naturally bifurcates into two sweeping branches. This unique point of division gives the tabletop a sculptural, organic silhouette, with flowing contours and grain patterns that ripple outward like the rings of time itself. The surface has been carefully planed to reveal the sycamore’s warm, pale hues, delicately accented by darker striations and intricate figuring that make every inch of the wood uniquely expressive. Retaining its natural live edge, the table preserves the raw elegance of the tree while offering a smooth, refined surface for everyday use. The craftsmanship honors the inherent character of the material rather than masking it, allowing nature’s artistry to take center stage. With its uncommon shape and rich texture, this coffee table becomes more than just a piece of furniture—it’s a conversation piece, a functional sculpture that carries the story of the tree it came from. Perfect for modern, rustic, or eclectic interiors, it adds warmth and authenticity to any living space, blending the timeless appeal of natural wood with a bold, contemporary design.

See the conversation here: https://chatgpt.com/share/68966b84-1954-8004-a7bd-d6e05ec7c20d 

## Features



## Lighthouse Reports and Validation

### Performance

### Accessibility

### Code Validation

### Code Documentation

## Testing

### Testing User Stories

####  I want To easily register for an account So that I can save account/address details or past orders
Steps:
1. Navigate to the homepage
2. Click "Register"
3. Provide email, username, and password (twice)
4. Click "Sign up"

Status: Pass - Toast notification lets the user know

####  I want recive an email confirming successful sign-up So that I know other email confirmations wont go directly to junk.
Steps:
1. Upon successfully completing the registration, find the "Confirm your account" email that gets set to the user's email address
2. Open the URL in the email
3. Account is verified - user is redirected to Log In page

Status - Pass - user can now log in


#### I want to easily log in/out So that to keep my details and orders safe at minimal inconvenience.
Steps:
1. With a verified account, visit the site and click "Log In"
2. While logged in, visit My Profile
3. Log out

Status - Pass

####  I want to be able to recover my account/password So that I don't lose my account/order history/wishlist items.

Steps:
1. Visit the login page
2. Click "Forgot Password?"
3. Provide the email of a registered account
4. A password reset email will be sent to that account
5. Click the link provided to reset the password
6. Log in with the new credentials

Status - pass

####  I want to be able to view a list of products So that I can select some products to purchase.
Steps:
1. Visit The Woodshed
2. View a Products List (All Products, Bowls, Chairs, Tables, Trinkets, Vases)

####  I want view more specific details about a product So that I can make an informed decision about price, material, finish, etc
Steps:
1. Visit The Woodshed and view a Products List (All Products, Bowls, Chairs, Tables, Trinkets, Vases)
2. Click "See More Details" on a Product Card

Status - Pass - More product details including price, material, finish, and a description are available

####  I want to see a gallery/carousel of images depicting a particular product So that I can see physical details not covered by basic stats.
Steps:
1. Visit The Woodshed and view a Products List (All Products, Bowls, Chairs, Tables, Trinkets, Vases)
2. Click "See More Details" on a Product Card
3. Click the images to the side of the main image to scroll the gallery in that direction
or
3. Click the main image to scroll the gallery to the right

Status - Pass

####  I want to be able to see products in a specific category So that I can more easily find products to fit my requirements
Steps:
1. Visit The Woodshed
2. Click one of the following options from the navigation bar - Bowls, Chairs, Tables, Trinkets, Vases

Status - Pass

####  I want to be able to add products to my wishlist So that I can save for later.
Steps:
1. Visit the Woodshed as a logged in user and view a Products List (All Products, Bowls, Chairs, Tables, Trinkets, Vases)
2. Decide on a product to add to the wishlist and click "Add to Wishlist"
Or
2. Click "See more details"
3. Click "Add to Wishlist"

####  I want to be able to add products from wishlist to basket, So that I can keep track of products that I like and buy them
Steps:
1. Visit the Woodshed as a logged in user and view a Products List (All Products, Bowls, Chairs, Tables, Trinkets, Vases)
2. Decide on a product to add to the basket and click "Add to Basket"
Or
2. Click "See more details"
3. Click "Add to Basket"
Or
1. Visit the Woodshed as a logged in user with an item already saved in the wishlist
2. Navigate to Wishlist
3. Click "add to basket" on a product

Status - Pass

####  I want to see my basket total So that I can avoid going over-budget.
1. Visit the Woodshed as a logged in user and view a Products List (All Products, Bowls, Chairs, Tables, Trinkets, Vases)
2. Decide on a product to add to the basket and click "Add to Basket"
3. Navigate to the Basket and scroll to the end of the list of products in the basket to the basket summary

Status - Pass

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



Add a page about comissioning a specific piece?

 -->