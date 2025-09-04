from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.db.models import Prefetch
from app.templatetags import stars_tags
# Create your views here.
def home(request):

    categories  = Category.objects.filter(parent_id__isnull = True,level=0)[:12].prefetch_related(
                    Prefetch("products", queryset=Product.objects.order_by("?")[:16], to_attr="limited_products")
                )
    products            = Product.objects.order_by('?')[:20]
    productsellers      = Product.objects.order_by('?')[:21]
    reviews             = Review.objects.order_by('?')[:20]

    context     = {
                    'categories' :categories,
                    'products' :products,
                    'productsellers' :productsellers,
                    'reviews' :reviews,
                }
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