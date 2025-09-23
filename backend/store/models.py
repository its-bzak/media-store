from django.db import models

# Create your models here.

class Media(models.Model):

    MEDIA_TYPES = [
        ('movie', 'Movie'),
        ('record', 'Record'),
        ('book', 'Book'),
        ('game', 'Video Game'),
    ]

    title = models.CharField(max_length=100)
    is_available = models.BooleanField()
    price = models.DecimalField(decimal_places=2, max_digits=6)
    genre = models.CharField(max_length=100)
    media_type = models.CharField(max_length=100, choices=MEDIA_TYPES)

    def __str__(self):
        return f"{self.title} ({self.media_type})"