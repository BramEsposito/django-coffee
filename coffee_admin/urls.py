from django.urls import path
from . import admin

app_name = 'coffee_admin'

urlpatterns = [
    # Add custom admin URLs here
    # path('dashboard/', admin.custom_admin_view, name='dashboard'),
]
