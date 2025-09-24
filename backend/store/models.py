from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Media(models.Model):

    MEDIA_TYPES = [
        ('movie', 'Movie'),
        ('record', 'Record'),
        ('book', 'Book'),
        ('game', 'Video Game'),
    ]


    title = models.CharField(max_length=100)
    buyprice = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    rentalprice = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    genre = models.CharField(max_length=100)
    media_type = models.CharField(max_length=100, choices=MEDIA_TYPES)
    stock_quantity = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.media_type})"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    preferred_genres = models.JSONField(default=list, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    loyalty_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username


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
        return f"Order {self.id} - {self.user.username}"

class OrderItem(models.Model):

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.media.title}"
