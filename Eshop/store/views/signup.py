from django.shortcuts import render, redirect
from store.models.customer import Customer
from django.contrib.auth.hashers import make_password
from django.views import View


class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        PostData = request.POST
        first_name = PostData.get('firstname')
        last_name = PostData.get('lastname')
        phone_no = PostData.get('phone')
        email = PostData.get('email')
        password = PostData.get('password')

        # Validation
        value = {'first_name': first_name,
                 'last_name': last_name,
                 'phone_no': phone_no,
                 'email': email
                 }

        error_msg = None

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone_no=phone_no,
                            email=email,
                            password=password
                            )
        error_msg = self.ValidateCustomer(customer)

        # saving
        if not error_msg:
            print(first_name, last_name, phone_no, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')

        else:
            data = {
                'error': error_msg,
                'values': value
            }
            return render(request, 'signup.html', data)

    def ValidateCustomer(self, customer):
        error_msg = None
        if not customer.first_name:
            error_msg = 'First name Required!!'
        elif len(customer.first_name) < 2:
            error_msg = 'first name must be 2 or more..'
        elif not customer.last_name:
            error_msg = 'Last name Required!!'
        elif len(customer.last_name) < 2:
            error_msg = 'first name must be 2 or more..'
        elif not customer.phone_no:
            error_msg = 'Phone no Required!!'
        elif len(customer.phone_no) < 10:
            error_msg = 'Phone number must have 10 Digits.'
        elif not customer.email:
            error_msg = 'Email Required!!'
        elif len(customer.email) < 12:
            error_msg = 'email must have 12 character.'
        elif not customer.password:
            error_msg = 'Password must be Required!!'
        elif len(customer.password) < 8:
            error_msg = 'password must have 8 or more length.'
        elif customer.isExist():
            error_msg = 'Email already registered.'

        return error_msg
