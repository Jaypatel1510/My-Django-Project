from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from store.models import customer
from store.models.product import Product

from store.templatetags import cart
from store.views.login import Login

class Cart(View):
    def get(self, request, order=None):
        if customer:
            cart_data = request.session.get('cart')
            if cart_data:
                ids = cart_data.keys()
                products = Product.get_products_by_id(ids)
                print(products)
            else:
                products = ["Do not exist"]  # No products in the cart

        else:
            if Login.return_url:
                return HttpResponseRedirect(Login.return_url)
            else:
                Login.return_url = None
                return redirect('cart')

        return render(request, 'cart.html', {'products': products})
