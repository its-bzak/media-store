from django.urls import path
from . import views

urlpatterns = [
    path('', views.media_list, name='media_list'),       # /media/
    path('about/', views.about, name='about'),           # /media/about/
    path('cart/', views.view_cart, name='view_cart'),     # /media/cart/
    path('<slug:slug>/', views.item_info, name='item_info'),  # /media/<slug>/
    path('register/', views.register, name='register'),
]
