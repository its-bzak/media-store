from django.urls import path
from . import views

urlpatterns = [
    path('', views.media_list, name='media_list'),       # /store/
    path('about/', views.about, name='about'),           # /store/about/
    path('cart/', views.view_cart, name='view_cart'),     # /store/cart/
    path('register/', views.register, name='register'), # / store/register/
    path('<slug:slug>/', views.item_info, name='item_info'),  # /store/<slug>/
]
