# Django Coffee Admin

A Django package designed to provide admin-only functionality without database models.

## Overview

This package demonstrates how to create a Django app that:
- Loads only in the Django Admin interface
- Requires no database models
- Provides custom admin views and functionality
- Can be easily integrated into any Django project

## Installation

```bash
pip install django-coffee-admin
```

Or install from source:

```bash
git clone https://github.com/BramEsposito/django-coffee.git
cd django-coffee
pip install -e .
```

## Quick Start

1. Add `'coffee_admin'` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'coffee_admin',
]
```

2. (Optional) Include coffee_admin URLs in your project's `urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/coffee/', include('coffee_admin.urls')),
]
```

3. Run your Django development server and access the admin interface.

## Features

- **No Models Required**: This package demonstrates admin functionality without database models
- **Custom Admin Views**: Includes example staff-only views
- **Easy Integration**: Simple installation and configuration
- **Extensible**: Easy to extend with your own admin functionality

## Documentation

For detailed documentation, see the [coffee_admin/README.md](coffee_admin/README.md) file.

## Use Cases

This package is useful when you need to:
- Add custom admin dashboard functionality
- Create admin-only tools and utilities
- Provide administrative interfaces without database storage
- Build custom reporting or monitoring dashboards

## Requirements

- Python 3.8+
- Django 3.2+

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request
