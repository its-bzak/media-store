from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Media, Customer, Order, OrderItem, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

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
    total = sum(item.get_total_price() for item in items)

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

def add_to_cart(request, slug):
    media_item = get_object_or_404(Media, slug=slug)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        media=media_item,
        defaults={'quantity': 1, 'price': media_item.price},
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('media_list')

def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('view_cart')

@login_required
@transaction.atomic
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()

    if not items:
        return redirect(request, 'store/checkout_empty.html')

    order = Order.objects.create(
        user=request.user,
        total_price=cart.get_total_price(),
        status='pending'
    )

    for item in items:
        OrderItem.objects.create(
            order=order,
            media=item.media,
            quantity=item.quantity,
            price=item.price,
        )

    cart.items.all().delete()

    return render(request, 'store/checkout_success.html', {'order': order})