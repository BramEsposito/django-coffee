from django.urls import path
from . import views

app_name = 'coffee_admin'

urlpatterns = [
    # Search endpoint for launcher
    path('search/', views.SearchAdminUrlsView.as_view(), name='search'),
    # Add custom admin URLs here
    # path('dashboard/', views.AdminDashboardView.as_view(), name='dashboard'),
]
