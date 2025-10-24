from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Media, Customer, Order, OrderItem, Cart


def media_list(request):
    """
    Displays all media items in the store.
    """
    media_items = Media.objects.all().order_by('title')
    return render(request, 'media/media_list.html', {'media_items': media_items})


def item_info(request, slug):
    # Displays a single media item's details.
    media_item = get_object_or_404(Media, slug=slug)
    return render(request, 'media/item_info.html', {'media_item': media_item})


def about(request):
    """
    To-do
    """
    return render(request, 'media/about.html')


def cart_view(request):
    """
    To-do shopping cart page
    (Will be implemented later using sessions or a Cart model.)
    """
    return render(request, 'media/cart.html')
