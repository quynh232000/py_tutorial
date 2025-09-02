from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request,'app/home.html')
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