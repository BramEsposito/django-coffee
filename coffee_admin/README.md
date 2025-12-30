# Coffee Admin

A Django package designed to be loaded only in the Admin interface, without any database models.

## Features

- Admin-only interface
- No database models required
- Custom admin views and functionality
- Easy integration with existing Django projects

## Installation

Add `'coffee_admin'` to your `INSTALLED_APPS` in your Django settings:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'coffee_admin',  # Add this line
]
```

## Usage

### Including in Admin URLs

Add the coffee_admin URLs to your main `urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/coffee/', include('coffee_admin.urls')),
]
```

### Custom Admin Views

The package includes example custom admin views that don't require models:

- `custom_admin_view`: A basic admin view example
- `admin_dashboard`: A staff-only dashboard view

### Extending the Package

You can extend this package by:

1. Adding custom admin views in `views.py`
2. Registering custom admin URLs in `urls.py`
3. Creating custom templates in `templates/coffee_admin/`
4. Adding business logic in the `ready()` method of `CoffeeAdminConfig`

## File Structure

```
coffee_admin/
├── __init__.py
├── admin.py           # Admin configuration and custom admin site
├── apps.py            # App configuration
├── urls.py            # URL routing for custom admin views
├── views.py           # Custom admin views
├── templates/
│   └── coffee_admin/
│       └── dashboard.html
└── README.md
```

## Requirements

- Django 3.2+
- Python 3.8+

## License

See main project LICENSE file.
