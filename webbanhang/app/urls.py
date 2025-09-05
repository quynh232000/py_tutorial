from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name='home'),
    path('cart', views.cart,name='cart'),
    path('san-pham/<slug:slug>', views.detail,name='detail'),
    path('testemonial', views.testemonial,name='testemonial'),
    path('checkout', views.checkout,name='checkout'),
    path('contact', views.contact,name='contact'),
    path('shop', views.shop,name='shop'),
    path('shop/<slug:slug>', views.shop,name='shop_detail'),
]