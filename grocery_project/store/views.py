from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from .models import Product, Cart, Order


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def register(request):
    if request.method == 'POST':
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        return redirect('login')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required

def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart_item, created = Cart.objects.get_or_create(
        product=product,
        user=request.user,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1

    cart_item.save()
    return redirect('cart')



@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user)
    total = sum(c.total_price() for c in carts)
    return render(request, 'cart.html', {'carts': carts, 'total': total})


@login_required
def checkout(request):
    carts = Cart.objects.filter(user=request.user)
    total = sum(c.total_price() for c in carts)

    if request.method == 'POST':
        Order.objects.create(
            user=request.user,
            total_amount=total,
            address=request.POST['address']
        )
    send_mail(
    'Order Confirmed - Grocery Store',
    f'Thank you for your order! Total amount: ₹{total}',
    'yourgmail@gmail.com',
    [request.user.email],
    fail_silently=True,
)
    carts.delete()
    return redirect('orders')

    return render(request, 'checkout.html', {'total': total})


@login_required
def orders_view(request):
    orders = Order.objects.all()
    return render(request, 'orders.html', {'orders': orders})



@staff_member_required
def admin_dashboard(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_sales = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    return render(request, 'admin_dashboard.html', {
        'products': total_products,
        'orders': total_orders,
        'sales': total_sales
    })

@login_required
def payment_view(request):
    carts = Cart.objects.filter(user=request.user)
    total = sum(c.total_price() for c in carts)
    return render(request, 'payment.html', {'total': total})
