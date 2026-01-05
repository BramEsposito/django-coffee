"""
URL configuration for testing
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/coffee/', include('coffee_admin.urls')),
    path('admin/', admin.site.urls),
]
