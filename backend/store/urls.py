from django.urls import path
from . import views

urlpatterns = [
    path('', views.media_list, name='media_list'),       # /store/
    path('cart/', views.view_cart, name='view_cart'),     # /store/cart/
    path('register/', views.register, name='register'), # / store/register/
    path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('buy-now/<slug:slug>/', views.buy_now, name='buy_now'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('orders/', views.order_history, name='order_history'),
    path('profile/', views.profile, name='profile'),
    path('require-email/', views.require_email, name='require_email'),
    path('checkout/', views.checkout, name='checkout'),
    path('<slug:slug>/', views.item_info, name='item_info'),  # /store/<slug>/
]
