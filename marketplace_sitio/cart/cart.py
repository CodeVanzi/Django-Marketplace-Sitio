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
                self.remove(product)
        if self.cart[product_id]['quantity'] == 0:
            self.remove(product)
        self.save()
        
    # def add(self, product, quantity=1, update_quantity=False):
    #     """
    #     Add a product to the cart or update its quantity.
    #     """
    #     product_id = str(product.id)
    #     if product_id not in self.cart:
    #         self.cart[product_id] = {'quantity': 0,
    #                                  'price': str(product.price),
    #                                  'id': product_id}
    #     if update_quantity:
    #         self.cart[product_id]['quantity'] += int(quantity)
    #         if self.cart[product_id]['quantity'] == 0:
    #             self.remove(product)
    #     if self.cart[product_id]['quantity'] == 0:
    #         self.remove(product)
    #     self.save()


        
    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            
    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
        
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def get_total_quantity(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    """"
    Lembrete: se o código não funcionar, rever a parte 7 e revisar o código. lembrar também que a princípio era esperado receber um valor de preço como centavos, e não um valor decimal. talvez seja necessário revisar o código para trabalhar com centavos.
    """
    

    
    
    