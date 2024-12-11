from django.shortcuts import render, redirect
from Services.models import Product



def new_product_view(request):
        products = Product.objects.all() 
        return render(request,'purchases.html',{'products': products})