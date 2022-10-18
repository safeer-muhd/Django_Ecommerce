import json
from django.http import JsonResponse
from app_1.forms import CustomUserForm
from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def index(request):
    products = Product.objects.filter(trending=1)
    return render(request,'app/index.html',{'products':products})

def register(request):
    forms = CustomUserForm()
    if request.method == 'POST':
        forms = CustomUserForm(request.POST)
        if forms.is_valid():
            forms.save()
            messages.success(request,'Registration Success You can Login Now..!')
            return redirect('/login')
    return render(request,'app/register.html',{'form':forms})

def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,'Logged in Successfully')
                return redirect('/')
            else:
                messages.error(request,'Invalid User Name or Password')
                return redirect('login')
        return render(request,'app/login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'Logged Out Successfully')
    return redirect('/')

def collection(request):
    category = Catagory.objects.filter(status=0)
    return render(request,'app/collection.html',{'category':category})

def collectionsview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products = Product.objects.filter(category__name=name)
        return render(request,'app/products/index.html',{'products':products,'category':name})
    else:
        messages.warning(request,'No Such Category Found')
        return redirect('collection')

def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products = Product.objects.filter(name=pname,status=0).first()
            return render(request,'app/products/product_details.html',{'products':products,'category':cname})
        else:
            messages.error(request,'No Such Products Found')
            return redirect('collection')
    else:
        messages.error(request,'No Such Category Found')
        return redirect('collection')

def add_to_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            prod_check = Product.objects.get(id=prod_id)
            if(prod_check):
                if(Cart.objects.filter(user=request.user.id,product_id=prod_id)):
                    return JsonResponse({'status':'Product Already in Cart'})
                else:
                    prod_qty = int(request.POST.get('product_qty'))
                    if prod_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user,product_id=prod_id,product_qty=prod_qty)
                        return JsonResponse({'status':'Product added successfully'})
                    else:
                        return JsonResponse({'status':'Only '+str(prod_check.quantity)+' quantity available'})
            else:
                return JsonResponse({'status':'No Such Products Found'})
        else:
            return JsonResponse({'status':'Login to Continue'})
    else:
        return JsonResponse({'status':'Invalid Access'}) 

def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,'app/cart.html',{'cart':cart})
    else:
        return redirect('/')

def remove_cart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user,product_id= prod_id)):
            cartitem = Cart.objects.get(product_id=prod_id,user=request.user)
            cartitem.delete()
        return JsonResponse({'status':'Deleted successfully'})
    return redirect('/cart')

def fav_page(request):
    return redirect('/')

def checkout_page(request):
    rawcart = Cart.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_qty > item.product.quantity:
            Cart.objects.delete(id=item.id)

    cartitem = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cartitem:
        total_price += item.product.selling_price * item.product_qty
        return render(request,'app/checkout.html',{'cartitems':cartitem,'total_price':total_price})
