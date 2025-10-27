"""
URL configuration for backend project.
"""

from django.contrib import admin
from django.urls import path, include
from pip._internal.network import auth

from store import views  # project-level views like home and about

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # Main site page
    path('', views.media_list, name='home'),

    # Store app URLs (everything under /media/)
    path('store/', include('store.urls')),

    #Authentication ie. User login, logout and signup
    path('accounts/', include('django.contrib.auth.urls')),
]

# Optional: handle static/media files in development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)