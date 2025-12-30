from django.urls import path
from . import views

app_name = 'coffee_admin'

urlpatterns = [
    # Search endpoint for launcher
    path('search/', views.search_admin_urls, name='search'),
    # Add custom admin URLs here
    # path('dashboard/', views.admin_dashboard, name='dashboard'),
]
