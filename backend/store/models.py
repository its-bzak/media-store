from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid

# == Media Model == #

class Media(models.Model):
    MEDIA_TYPES = [
        ('movie', 'Movie'),
        ('record', 'Record'),
        ('book', 'Book'),
        ('game', 'Video Game'),
    ]

    title = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    genre = models.CharField(max_length=100)
    media_type = models.CharField(max_length=100, choices=MEDIA_TYPES)
    stock_quantity = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        """Generate unique slug"""
        if not self.slug:
            base_slug = slugify(self.title)
            unique_id = uuid.uuid4().hex[:6]
            self.slug = f"{base_slug}-{unique_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.media_type})"

    class Meta:
        ordering = ['title']

# == Customer Model == #

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    preferred_genres = models.JSONField(default=list, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    loyalty_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username if self.user else "Guest Customer"

# == Cart + CartItem Models == #

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=6, default=0)

    def __str__(self):
        return f"{self.media.title} × {self.quantity}"

    def get_total_price(self):
        return self.media.price * self.quantity

# == Order + OrderItem Models == #

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Order Pending'),
        ('completed', 'Order Completed'),
        ('canceled', 'Order Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE, null=True)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('cart', 'media')

    def __str__(self):
        return f"{self.quantity} × {self.media.title}"

