from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name='home'),
    path('shop', views.shop,name='shop'),
    path('cart', views.cart,name='cart'),
    path('detail', views.detail,name='detail'),
    path('testemonial', views.testemonial,name='testemonial'),
    path('checkout', views.checkout,name='checkout'),
    path('contact', views.contact,name='contact'),
]