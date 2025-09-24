from django.forms import Media
from django.shortcuts import render
from .models import Media


# Create your views here.

def media_list(request):
    media_items = Media.objects.all()
    return render(request, 'media/media_list.html', {'media_items': media_items})