from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Media, Customer, Order, OrderItem, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from .forms import EmailUpdateForm

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

@login_required(login_url='login')
def buy_now(request, slug):
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

    return redirect('checkout')


@login_required(login_url='login')
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
        return render(request, 'store/checkout_empty.html')

    if not request.user.email:
        return redirect('require_email')
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
        item.media.stock_quantity = max(0, item.media.stock_quantity - item.quantity)
        item.media.save()

    cart.items.all().delete()

    send_mail(
        subject="Your Media Store Order Confirmation",
        message=f"Hi {request.user.first_name or request.user.username},\n\n"
                f"Thank you for your order! Your order id is: #{order.id}! "
                f"Your total was ${order.total_price}. "
                f"We hope you'll shop again soon!\n\n– Media Store Team",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[request.user.email],
        fail_silently=True,
    )

    return render(request, 'store/checkout_success.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import ProfileForm, CustomerPreferencesForm

@login_required
def profile(request):
    customer, created = Customer.objects.get_or_create(user=request.user)

    profile_form = ProfileForm(request.POST or None, instance=request.user)
    prefs_form = CustomerPreferencesForm(request.POST or None, instance=customer)
    password_form = PasswordChangeForm(request.user, request.POST or None)

    if request.method == 'POST':
        if 'save_profile' in request.POST:
            if profile_form.is_valid() and prefs_form.is_valid():
                profile_form.save()
                prefs_form.save()
                return redirect('profile')

        elif 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                return redirect('profile')

    return render(request, 'store/profile.html', {
        'profile_form': profile_form,
        'prefs_form': prefs_form,
        'password_form': password_form,
    })


@login_required
def require_email(request):
    """Ask the user to provide an email before checkout."""
    if request.user.email:
        # Already has an email → skip directly to checkout
        return redirect('checkout')

    if request.method == 'POST':
        form = EmailUpdateForm(request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.save()
            return redirect('checkout')
    else:
        form = EmailUpdateForm()

    return render(request, 'store/require_email.html', {'form': form})