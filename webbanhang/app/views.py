from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.db.models import Prefetch,Count
from app.templatetags import stars_tags
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
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
def shop(request,slug = None):
    category        = None
    sort            = request.GET.get("sort", "")
    price_max       = request.GET.get("price_max")
    if slug :
        category    = get_object_or_404(
                        Category.objects.annotate(product_count=Count("products")),
                        slug=slug
                    )
    categories      = (
                        Category.objects.filter(parent_id__isnull=True, level=0)
                        .annotate(product_count=Count("products"))
                    )
    
    if slug:
        category        = get_object_or_404(Category, slug=slug)
        product_list    = Product.objects.filter(category_id=category.id).order_by("?")
    else:
        category        = None
        product_list    = Product.objects.order_by("?")

    # lọc theo giá
    if price_max and price_max.isdigit():
        product_list = product_list.filter(price__lte=int(price_max))

    # Áp dụng sort
    if sort == "newest":
        product_list = product_list.order_by("-created_at")   # cần field created_at
    elif sort == "oldest":
        product_list = product_list.order_by("created_at")
    elif sort == "price_asc":
        product_list = product_list.order_by("price")
    elif sort == "price_desc":
        product_list = product_list.order_by("-price")

    # phân trang (12 sp mỗi trang)
    paginator = Paginator(product_list, 12)
    page_number = request.GET.get("page")  # lấy số trang từ query string
    products = paginator.get_page(page_number)  # trả về Page object

    # noi bat
    features = Product.objects.order_by("?")[:4]
    params = {
        'categories': categories,
        "category":category,
        "products":products,
        "sort": sort,  
        'features':features 
    }


    return render(request,'app/shop.html',params)
def cart(request):
    return render(request,'app/cart.html')
def checkout(request):
    return render(request,'app/checkout.html')
def testemonial(request):
    reviews             = Review.objects.order_by('?')[:20]
    return render(request,'app/testemonial.html',{"reviews":reviews})
def detail(request,slug):
    return render(request,'app/detail.html')
def contact(request):
    return render(request,'app/contact.html')