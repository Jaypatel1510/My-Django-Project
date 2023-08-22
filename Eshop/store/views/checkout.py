from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from store.models.product import Product
from store.models.customer import Customer
from store.models.orders import Order
from store.views.login import Login

from store.templatetags import cart


class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))

            if customer:
                order.save()
                print(order.placeOrder())
                request.session['cart'] = {}
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('cart')
            else:
                error_msg = 'Email or Password is Invalid.'
            return render(request, 'login.html', {'error': error_msg})
            if Login.return_url:
                return HttpResponseRedirect(Login.return_url)
            else:
                Login.return_url = None
                return redirect('cart')
        return redirect('cart')

