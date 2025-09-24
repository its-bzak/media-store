from django.urls import path
from . import views

urlpatterns = [
    path('', views.media_list, name='media'),
    path('<slug:slug>', views.media_page, name='page')
]