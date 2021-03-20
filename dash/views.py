from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import  Product,Category,ContactUs,Cart
from .models import SignUp
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.core.paginator import Paginator

import json
# Create your views here.
def home(req):
    items=Product.objects.all()
    items=list(items)
    if len(items)>10:
        items=items[:10]
    d={'items':items}
    return render(req,'index.html' , d)
def about(req):
    return render(req,'about.html')
def contact(req):
    return render(req,'contacts.html')
@login_required()
@csrf_exempt
def AddToCart(req):
    print("inside add to cart")
    if req.user.is_authenticated:
        if req.method=='POST':
            pid=req.POST.get('id')
            if pid is None:
                return JsonResponse({'success':False})
            pid=int(pid)
            print("pid = {}".format(pid))
            is_exist=Cart.objects.filter(product__id=pid,user__id=req.user.id,status=False)
            if len(is_exist)>0:
                return JsonResponse({'success':True})
            else:
                product=get_object_or_404(Product,id=pid)
                user=get_object_or_404(User,id=req.user.id)
                cart=Cart(user=user,product=product)
                cart.save()
                return JsonResponse({'success':True})
    return JsonResponse({'sucess':False})
@csrf_exempt

def checkout(req):
    if not req.user.is_authenticated:
        return render(req,'SignUp-login.html')

    order_list=[]
    cartItems=Cart.objects.filter(user__id=req.user.id)
    for product in cartItems:
        order_list.append(product.product)
    total=50
    for product in order_list:
        total+=int(product.price)
    return render(req,'checkout.html',{'products':order_list,'total':total})
@csrf_exempt
@login_required()
def removecartItems(req):
    print("inside removecartItems")
    if req.method=='POST':

        if req.user.is_authenticated:
            id=req.POST['id']
            print(id)
            cart=get_object_or_404(Cart,product__id=id)
            print(cart)
            if cart is not None:

                cart.delete()
                print('object deleted')
                order_list=[]
                cartItems=Cart.objects.filter(user__id=req.user.id)
                for product in cartItems:
                    order_list.append(product.product)
                total=50
                for product in order_list:
                    total+=int(product.price)
                return JsonResponse({'success':True,'total':total})


    return JsonResponse({'success':False})
def thankyou(req):
    if req.method=='POST':
        email=req.POST['email']
        tel=req.POST['tel']
        full_name=req.POST['name']
        address=req.POST['address']
        city=req.POST['city']
        state=req.POST['state']
        country=req.POST['country']
        poster_code=req.POST['postal']
        print(email,tel,full_name,address,country,city,state,poster_code)
        return  render(req,'ThankYou.html')
    return render(req,'index.html')
@csrf_exempt
def contactUs(req):
    if req.method=='POST':
        name=req.POST.get('name')
        phone=req.POST.get('phone')
        message=req.POST.get('message')
        email=req.POST.get('email')
        print(name,email,phone,message)
        if email is not None and message is not None and phone is not None and name is not None:

            ContactUs(name=name,email=email,number=phone,message=message).save()
            print("inside contact us")
            return JsonResponse({'success':True})
    print("else part")

    return JsonResponse({'success':False})
def SignUplogin(req):
    if req.method=='POST':
        if 'signup' in req.POST:
            username=req.POST['username']
            email=req.POST['email']
            password=req.POST['password']
            try:
                print(email,username,password)
                if email not in User.objects.filter(email__contains=email):

                    user=User.objects.create_user(email=email,password=password,username=email)
                    print('user created')
                    SignUp.objects.create(user=user)
                    auth.login(req,user)
                    return redirect('home')
            except :

                print("something went wrong")
            return render(req,'index.html')
        elif 'login' in req.POST:
            username=req.POST['Username']
            password=req.POST['Password']
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(req, user)
        return redirect('home')



    return render(req,'SignUp-login.html')
def search(req):
    if req.method=='GET':
        query=req.GET.get('search')
        if query is None:
            return  render(req,'index.html')
        search_result=Product.objects.filter(name__contains=query)
        search_des=Product.objects.filter(description__contains=query)
        search_price=Product.objects.filter(price__contains=query)
        search_cat_des=Category.objects.filter(description__contains=query)
        return render(req,'search.html',{'search_result':search_result,'search_des':search_des,'search_price':search_price,'search_cat_des':search_cat_des})
    return  render(req,'index.html')

def shopSingle(req,pk):
    if req.user.is_authenticated:

        product=Product.objects.filter(pk=pk)
        items=Product.objects.all()

        cartItems=Cart.objects.filter(product__id=pk)

        d = {'products': items , 'product': product,'cartItems':cartItems}
        return render(req,'shop-single.html', d)
    return render(req,'SignUp-login.html')
def product(req):
    items=Product.objects.all().order_by('id')
    l=list(items)
    date_wise_sorted_list=sorted(l,key=lambda x:x.date,reverse=True)
    print(date_wise_sorted_list)
    paginator=Paginator(items,4)
    page_number=req.GET.get('page')
    page_obj=paginator.get_page(page_number)

    d={'items':page_obj,'new_product':date_wise_sorted_list}
    return render(req,'shop.html',d)
@login_required()
def logout(req):
    auth.logout(req)
    return redirect('home')
def blogSingle(req):
    return  render(req,'sindle-blog.html')
@login_required()
def gallery(req):
    return render(req,'gallery.html'),
def services(req):
    return render(req,'services.html')
def privacyPolicy(req):
    return render(req,'pravicy-policy.html')

