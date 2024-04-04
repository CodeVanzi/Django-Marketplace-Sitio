from decimal import Decimal
from django.conf import settings


from product.models import Product

class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        
    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)
            
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
            


            
    def __len__(self):

        return sum(item['quantity'] for item in self.cart.values())
    
    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True
            
    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price),
                                     'id': product_id}
        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)
            if self.cart[product_id]['quantity'] == 0:
                self.remove(product_id)
        if product_id not in self.cart:
            print('não está no carrinho')
        self.save()

        
    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            
    def remove_all(self, product_id):
        product_id = str(product_id)  # Define the "product_id" variable
        for item_id in list(self.cart.keys()):
            if self.cart[item_id]['id'] == product_id:  # Use the "product_id" variable
                del self.cart[item_id]
        self.save()
            
    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
        
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def get_total_quantity(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_item(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            return self.cart[str(product_id)]
        else:
            return None

    
    
    