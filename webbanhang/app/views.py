from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.db.models import Prefetch,Count
from app.templatetags import stars_tags
from django.shortcuts import get_object_or_404,redirect
from django.core.paginator import Paginator



from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms.forms import RegisterForm
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

    search          = request.GET.get("search")
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
    elif search:
        # lọc theo search (tìm tên sản phẩm chứa từ khóa)
        category = None
        product_list = Product.objects.filter(name__icontains=search).order_by("?")
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
    paginator   = Paginator(product_list, 12)
    page_number = request.GET.get("page")  # lấy số trang từ query string
    products    = paginator.get_page(page_number)  # trả về Page object

    # noi bat
    features    = Product.objects.order_by("?")[:4]
    params      = {
                    'categories': categories,
                    "category":category,
                    "products":products,
                    "sort": sort,  
                    'features':features 
                }


    return render(request,'app/shop.html',params)
def cart(request):
    cart        = request.session.get("cart", {})
    
    for id,item in cart.items():
        item['total'] = item['quantity'] * item['price']
    
    total       = sum(item["price"] * item["quantity"] for item in cart.values())
    
    return render(request,'app/cart.html',{
        'cart':cart,
        'total':total
    })
def checkout(request):
    cart        = request.session.get("cart", {})
    
    for id,item in cart.items():
        item['total'] = item['quantity'] * item['price']
    
    total       = sum(item["price"] * item["quantity"] for item in cart.values())
    
    return render(request,'app/checkout.html',{
        'cart':cart,
        'total':total
    })
def testemonial(request):
    reviews             = Review.objects.order_by('?')[:20]
    return render(request,'app/testemonial.html',{"reviews":reviews})
def detail(request,slug):
    product         = get_object_or_404(
                        Product,
                        slug=slug
                    )
    
    categories      = (
                        Category.objects.filter(parent_id__isnull=True, level=0)
                        .annotate(product_count=Count("products"))
                    )

    relatives       = Product.objects.filter(category_id=product.category_id).order_by("?")[:5]
    relatives_pro   = Product.objects.filter(category_id=product.category_id).order_by("?")[:20]
    return render(request,'app/detail.html',{'product':product,'relatives':relatives,'categories':categories,'relatives_pro':relatives_pro})
def contact(request):
    return render(request,'app/contact.html')

def add_to_cart(request,product_id):
    product         = get_object_or_404(Product, id=product_id)

    cart            = request.session.get("cart", {})

    if str(product_id) in cart:
        cart[str(product_id)]["quantity"] += 1
    else:
        cart[str(product_id)]   = {
                                    "name": product.name,
                                    "price": product.price,
                                    "quantity": 1,
                                    "image":product.image,
                                    "slug":product.slug,
                                }

    request.session["cart"] = cart
    request.session.modified = True  # báo cho Django biết session đã thay đổi

    referer = request.META.get("HTTP_REFERER")
    if referer:
        return redirect(referer)
    return redirect("cart")

def update_cart(request,type,product_id,quantity):
    cart =request.session.get('cart',{})

    def add():
        eid = str(product_id)
        if eid in cart :
            cart[str(product_id)]['quantity']   += int(quantity)
        else:
            product                 = get_object_or_404(Product, id=product_id)
            cart[str(product_id)]   = {
                                        "name": product.name,
                                        "price": product.price,
                                        "quantity": 1,
                                        "image":product.image,
                                        "slug":product.slug,
                                    }
    def minus():
        if cart[str(product_id)]['quantity'] == 1:
            del cart[str(product_id)]
        else:

            cart[str(product_id)]['quantity']       -= int(quantity)
    
    def remove():
        del cart[str(product_id)]
    
    actions                         = {
                                        'add':add,
                                        'minus':minus,
                                        'remove':remove
                                    }   
    if type in actions:
        actions[type]()
    request.session["cart"]         = cart
    request.session.modified        = True
    return redirect("cart")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # mã hoá mật khẩu
            user.save()
            messages.success(request, "Đăng ký thành công! Hãy đăng nhập.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "app/register.html", {"form": form})
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # đổi "home" thành trang bạn muốn
        else:
            messages.error(request, "Sai tài khoản hoặc mật khẩu")
    return render(request, "app/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")

    