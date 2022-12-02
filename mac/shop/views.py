from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Product, Contact, Cart, Order, Customer
from math import ceil
from django.http import JsonResponse
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.views import View
from django.contrib import messages


# Create your views here.0

def index(request):
    allProds = []
    catprods = Product.objects.values("category", "id")
    cats = {item["category"] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, "shop/index.html", params)


def about(request):
    return render(request, "shop\\about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, "shop\\contact.html")

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'shop/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Updated Successfully!!')
        return render(request, "shop\\profile.html", {'form': form, 'active': 'btn-primary'})


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, "shop\\address.html", {'add':add})


class CustomerRegister(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "shop\\register.html", {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Registered Successfully!!')
            form.save()
        return render(request, "shop\\register.html", {'form': form})


def search(request):
    return render(request, "shop\\search.html")


def productView(request, myid):
    product = Product.objects.filter(id=myid)
    print(product)
    return render(request, "shop\\prodview.html", {"product": product[0]})


def checkout(request):
    user = request.user
    cart_sum = Cart.objects.filter(user=user)
    add = Customer.objects.filter(user=user)
    l = len(cart_sum)
    amount = 0
    total_amount = 0
    cart_product = [p for p in Cart.objects.all() if p.user==user]
    if cart_product:
        for p in cart_product:
            temp_amount = (p.product.price * p.quantity)
            amount += temp_amount
            total_amount = amount

    return render(request, "shop\\checkout.html", {'total_amount': total_amount, "cart_sum": cart_sum, "l": l, 'add':add})


def carts(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    try:
        cart_exist = Cart.objects.get(user=user, product=product_id)
        product_id = None
    except:
        try:
            product = Product.objects.get(id=product_id)
            Cart(user=user, product=product).save()
        except Product.DoesNotExist:
            product = None

    return redirect('/shop/Showcarts/')


def showcart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        total_amount = 0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                temp_amount = (p.product.price * p.quantity)
                amount += temp_amount
                total_amount = amount
            return render(request, 'shop/cart.html',
                          {"carts": cart, "total_amount": total_amount, "temp_amount": temp_amount,})
        else:
            return render(request, 'shop/cart.html')


def plusCart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(user=request.user, product=prod_id))
        c.quantity += 1
        c.save()
        amount = 0
        total_amount = 0
        cart_product = [p for p in Cart.objects.filter(user=request.user)]
        # if cart_product:
        for p in cart_product:
            temp_amount = (p.product.price * p.quantity)
            amount += temp_amount
            total_amount = amount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': total_amount
        }
    return JsonResponse(data)


def minCart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(user=request.user, product=prod_id))
        c.quantity = c.quantity - 1
        c.save()
        amount = 0
        total_amount = 0
        cart_product = [p for p in Cart.objects.filter(user=request.user)]
        # if cart_product:
        for p in cart_product:
            temp_amount = (p.product.price * p.quantity)
            amount += temp_amount
            total_amount = amount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': total_amount
        }
    return JsonResponse(data)


def revCart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(user=request.user, product=prod_id))
        c.delete()
        amount = 0
        total_amount = 0
        cart_product = [p for p in Cart.objects.filter(user=request.user)]
        # if cart_product:
        for p in cart_product:
            temp_amount = (p.product.price * p.quantity)
            amount += temp_amount
            total_amount = amount
        data = {
            'amount': amount,
            'total_amount': total_amount
        }
    return JsonResponse(data)

def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        Order(user=user, customer=customer, items=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')

def orders(request):
    user= request.user
    op = Order.objects.filter(user=user)
    return render(request, "shop/order.html", {'order':op})