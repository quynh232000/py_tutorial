from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user  = models.OneToOneField(User,on_delete=models.SET_NULL, null=True,blank=False)
    name  = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name or str(self.user)


class Category(models.Model):
    name  = models.CharField(max_length=255, null=True)
    slug  = models.SlugField(max_length=255, unique=True, null=True)
    image = models.ImageField(upload_to="categories/", null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,related_name="products")
    name        = models.CharField(max_length=255)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    image       = models.ImageField(upload_to="products/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating      = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        (0, "Pending"),
        (1, "Paid"),
        (2, "Shipped"),
        (3, "Completed"),
        (4, "Cancelled"),
    )

    customer   = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status     = models.IntegerField(choices=STATUS_CHOICES, default=0)
    order_code = models.CharField(max_length=255, null=True, blank=True)
    total      = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping   = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    first_name   = models.CharField(max_length=255, null=True, blank=True)
    last_name    = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    address      = models.CharField(max_length=255, null=True, blank=True)
    city         = models.CharField(max_length=255, null=True, blank=True)
    country      = models.CharField(max_length=255, null=True, blank=True)
    zip_code     = models.CharField(max_length=255, null=True, blank=True)
    phone        = models.CharField(max_length=255, null=True, blank=True)
    email        = models.EmailField(max_length=255, null=True, blank=True)
    note         = models.TextField(null=True, blank=True)
    payment_method = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer}"


class OrderItem(models.Model):
    order     = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product   = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity  = models.PositiveIntegerField(default=1)
    price     = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # snapshot price
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} x {self.quantity}"
