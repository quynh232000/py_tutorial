def cart_context(request):
    cart            = request.session.get('cart',{})
    total_quantity  = sum(item["quantity"] for item in cart.values())
    return {
        'cart':cart,
        'count_cart':len(cart),
        'total_quantity':total_quantity
    }