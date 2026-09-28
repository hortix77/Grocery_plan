from atexit import register
from turtle import home
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add/<int:id>/', add_to_cart, name='add'),
    path('cart/', cart_view, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('payment/', payment_view, name='payment'),
    path('orders/', orders_view, name='orders'),
    path('dashboard/', admin_dashboard, name='dashboard'),
    

]
