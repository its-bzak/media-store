from django.urls import path
from . import views

urlpatterns = [
    path('', views.media_list, name='media_list'),       # /media/
    path('about/', views.about, name='about'),           # /media/about/
    path('cart/', views.cart_view, name='cart_view'),    # /media/cart/
    path('<slug:slug>/', views.media_page, name='media_page'),  # /media/<slug>/
]
