"""
URL configuration for backend project.
"""

from django.contrib import admin
from django.urls import path, include
from . import views  # project-level views like home and about

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # Main site pages (home & about)
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # Store app URLs (everything under /media/)
    path('store/', include('store.urls')),
]

# Optional: handle static/media files in development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)