# Coffee Admin

A Django package designed to be loaded only in the Admin interface, without any database models.

## Features

- Admin-only interface
- No database models required
- Custom admin views and functionality
- Automatic JavaScript loading on every admin page
- Easy integration with existing Django projects

## Installation

Add `'coffee_admin'` to your `INSTALLED_APPS` in your Django settings:

**IMPORTANT:** For the JavaScript to load on every admin page, `coffee_admin` must be listed **before** `django.contrib.admin` in `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'coffee_admin',  # Must be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Run collectstatic to gather static files:

```bash
python manage.py collectstatic
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

### JavaScript Integration

The package automatically loads a JavaScript file (`coffee_admin.js`) on every admin page. This file includes:

- A stub implementation ready for customization
- Console logging to verify it's loaded
- A global `CoffeeAdmin` object for extending functionality

The JavaScript file is located at: `static/coffee_admin/js/coffee_admin.js`

You can customize this file to add your own admin UI enhancements, event handlers, or custom functionality that should run on every admin page.

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
├── static/
│   └── coffee_admin/
│       └── js/
│           └── coffee_admin.js  # Auto-loaded on every admin page
├── templates/
│   ├── admin/
│   │   └── base_site.html       # Template override for JS loading
│   └── coffee_admin/
│       └── dashboard.html
└── README.md
```

## Requirements

- Django 3.2+
- Python 3.8+

## License

See main project LICENSE file.
