from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.db.models import Prefetch

# Create your views here.
def home(request):
    categories  = Category.objects.all()

    categories = Category.objects.prefetch_related(
        Prefetch("products", queryset=Product.objects.order_by("?")[:8], to_attr="limited_products")
    )


    context     = {
                    'categories' :categories
                }
    print(categories)
    return render(request,'app/home.html',context)
def shop(request):
    return render(request,'app/shop.html')
def cart(request):
    return render(request,'app/cart.html')
def checkout(request):
    return render(request,'app/checkout.html')
def testemonial(request):
    return render(request,'app/testemonial.html')
def detail(request):
    return render(request,'app/detail.html')
def contact(request):
    return render(request,'app/contact.html')