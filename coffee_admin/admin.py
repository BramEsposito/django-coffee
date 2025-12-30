from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponse


class CoffeeAdminSite(admin.AdminSite):
    """
    Custom admin site for Coffee Admin package.
    This demonstrates a custom admin interface without models.
    """
    site_header = 'Coffee Administration'
    site_title = 'Coffee Admin'
    index_title = 'Welcome to Coffee Admin'


# Custom admin view example (no model required)
def custom_admin_view(request):
    """
    Example of a custom admin view that doesn't require a model.
    """
    context = {
        'title': 'Coffee Admin Dashboard',
        'site_header': 'Coffee Administration',
    }
    return render(request, 'admin/base_site.html', context)


# Register custom admin views
# You can add custom admin views here that don't require models
