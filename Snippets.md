<!-- Add Product o Cart using Session -->
Certainly! Here's an example of a simple Django code snippet that demonstrates adding a product to the cart:

```python

from django.shortcuts import render, redirect
from .models import Product

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    
    # Check if the cart is already stored in the session, or create a new one
    cart = request.session.get('cart', {})
    
    # Add the product to the cart or increment its quantity if it already exists
    cart[product_id] = cart.get(product_id, 0) + 1
    
    # Store the updated cart back in the session
    request.session['cart'] = cart
    
    return redirect('cart')  # Redirect to the cart page or any other desired page
```
