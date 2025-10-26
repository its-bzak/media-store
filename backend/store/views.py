from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Media, Customer, Order, OrderItem, Cart
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def media_list(request):
    """
    Displays all media items in the store.
    """
    media_items = Media.objects.all().order_by('title')
    return render(request, 'store/media_list.html', {'media_items': media_items})


def item_info(request, slug):
    # Displays a single media item's details.
    media_item = get_object_or_404(Media, slug=slug)
    return render(request, 'store/item_info.html', {'media_item': media_item})


def about(request):
    """
    To-do
    """
    return render(request, 'store/about.html')


def cart_view(request):
    """
    To-do shopping cart page
    (Will be implemented later using sessions or a Cart model.)
    """
    return render(request, 'store/cart.html')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = cart.get_total_price()

    return render(request, 'store/cart.html', {
        'cart': cart,
        'items': items,
        'total': total
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('media_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})