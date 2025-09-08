from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name='home'),
    path('cart', views.cart,name='cart'),
    path('register', views.register,name='register'),
    path('login', views.login,name='login'),
    path("logout/", views.logout, name="logout"),

    path('testemonial', views.testemonial,name='testemonial'),
    path('checkout', views.checkout,name='checkout'),
    path('contact', views.contact,name='contact'),
    path('shop', views.shop,name='shop'),
    path('shop/<slug:slug>', views.shop,name='shop_detail'),
    path('search/<str:search>', views.shop,name='search'),
    path('san-pham/<slug:slug>', views.detail,name='detail'),
    path('add_to_cart/<int:product_id>', views.add_to_cart,name='add_to_cart'),
    path('update_cart/<str:type>/<int:product_id>/<int:quantity>/', views.update_cart,name='update_cart'),
]