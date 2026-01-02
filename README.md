# Django Coffee Admin

A Django package that provides a Spotlight/Alfred-style command launcher for the Django admin interface, without requiring any database models.

## Features

- 🚀 **Spotlight/Alfred-style Launcher** - Quick command palette with keyboard shortcuts
- 🔍 **Real-time Search** - Search through all admin models and actions
- ⌨️ **Keyboard Navigation** - Full keyboard support (Ctrl+D, Arrow keys, Enter)
- 🎨 **Beautiful UI** - Modern, polished interface with smooth animations
- 🔌 **No Models Required** - Admin-only functionality without database tables
- 🎯 **Custom AdminSite Support** - Works with multiple admin sites
- 📦 **Easy Integration** - Simple installation and configuration

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

### 1. Add to INSTALLED_APPS

**IMPORTANT:** `coffee_admin` must be listed **before** `django.contrib.admin` for template overrides to work.

```python
INSTALLED_APPS = [
    'coffee_admin',  # Must come BEFORE django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

### 2. Include URLs

Add coffee_admin URLs to your project's `urls.py`:

**IMPORTANT:** The `coffee_admin` URL pattern must be registered **before** the main `admin/` URL pattern.

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Coffee admin URLs FIRST (more specific path)
    path('admin/coffee/', include('coffee_admin.urls')),
    # Generic admin URLs AFTER (less specific path)
    path('admin/', admin.site.urls),
]
```

**Why this order matters:** Django matches URLs from top to bottom. If `path('admin/', ...)` comes first, it will match `/admin/coffee/search/` and try to route it as a model URL, causing a 404 error. By placing the more specific `admin/coffee/` pattern first, it gets matched correctly.

### 3. Collect Static Files

```bash
python manage.py collectstatic
```

### 4. Start Using!

1. Log into Django admin
2. Press **Ctrl+D** anywhere in the admin
3. Start typing to search (e.g., "users", "groups")
4. Use **↑↓** arrow keys to navigate results
5. Press **Enter** to go to the selected page

## Usage

### Launcher Keyboard Shortcuts

- **Ctrl+D** - Toggle launcher
- **ESC** - Close launcher
- **↑** / **↓** - Navigate through results
- **Enter** - Select highlighted result and navigate
- Type to search in real-time

### Search API

The package provides a JSON API endpoint for searching admin URLs:

**Endpoint:** `/admin/coffee/search/`

**Query Parameters:**
- `q` - Search query (optional)

**Example Request:**
```bash
curl "http://localhost:8000/admin/coffee/search/?q=user"
```

**Example Response:**
```json
{
  "results": [
    {
      "title": "Users",
      "subtitle": "View all users",
      "url": "/admin/auth/user/",
      "icon": "👤",
      "category": "models",
      "app_label": "auth"
    },
    {
      "title": "Add User",
      "subtitle": "Create a new user",
      "url": "/admin/auth/user/add/",
      "icon": "➕",
      "category": "actions",
      "app_label": "auth"
    }
  ],
  "query": "user",
  "count": 2
}
```

### JavaScript API

The package exposes a global `CoffeeAdmin` object:

```javascript
window.CoffeeAdmin.showLauncher()    // Show the launcher
window.CoffeeAdmin.hideLauncher()    // Hide the launcher
window.CoffeeAdmin.toggleLauncher()  // Toggle launcher visibility
```

### Custom Admin Sites

Coffee Admin supports Django's custom `AdminSite` implementations:

```python
# myapp/admin.py
from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    site_header = 'My Custom Admin'
    name = 'myadmin'

my_admin = MyAdminSite()
```

```python
# urls.py
from coffee_admin.views import SearchAdminUrlsView
from myapp.admin import my_admin

urlpatterns = [
    path('myadmin/', my_admin.urls),
    path('myadmin/coffee/search/',
         SearchAdminUrlsView.as_view(admin_site=my_admin)),
]
```

For detailed examples with multiple admin sites and advanced configurations, see [docs/CUSTOM_ADMIN_SITES.md](docs/CUSTOM_ADMIN_SITES.md).

## Advanced Usage

### Customizing the Keystroke

You can customize the launcher keystroke by modifying the JavaScript configuration:

```javascript
// In your custom template or admin JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Change to Alt+K instead of Ctrl+D
    // (requires modifying coffee_admin.js directly)
});
```

### Extending the Package

You can extend this package by:

1. **Custom Admin Views** - Add views in `views.py`
2. **Custom URLs** - Register URLs in `urls.py`
3. **Custom Templates** - Create templates in `templates/coffee_admin/`
4. **Custom Styling** - Override CSS in `static/coffee_admin/css/`
5. **Custom AdminSites** - Use with multiple admin sites

## File Structure

```
coffee_admin/
├── __init__.py
├── admin.py              # Admin configuration
├── apps.py               # App configuration
├── urls.py               # URL routing (/search/ endpoint)
├── views.py              # Class-based views and search API
├── static/
│   └── coffee_admin/
│       ├── css/
│       │   └── launcher.css      # Launcher UI styles
│       └── js/
│           └── coffee_admin.js   # Launcher and keyboard shortcuts
├── templates/
│   ├── admin/
│   │   └── base_site.html        # Template override for JS/CSS loading
│   └── coffee_admin/
│       └── dashboard.html
└── README.md
```

## How It Works

1. **Template Override**: Extends Django's `admin/base.html` to inject CSS and JavaScript
2. **Keyboard Listener**: Listens for Ctrl+D globally in admin pages
3. **Launcher UI**: Creates a modal overlay with search input
4. **Debounced Search**: Makes API requests with 300ms debounce
5. **Real-time Results**: Displays filtered admin URLs with icons
6. **Navigation**: Navigate with keyboard or mouse, press Enter to go

## Use Cases

This package is useful when you need to:

- **Quick Navigation** - Jump to any admin page without clicking through menus
- **Search Admin Models** - Find models by name across all installed apps
- **Keyboard-First Workflow** - Navigate admin without touching the mouse
- **Custom Admin Tools** - Build admin utilities without database models
- **Multiple Admin Sites** - Support different admin interfaces in one project

## Requirements

- Python 3.8+
- Django 3.2+

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Development & Testing

### Installing Development Dependencies

To set up the development environment with testing tools:

```bash
pip install -e ".[dev]"
```

This installs:
- pytest - Testing framework
- pytest-django - Django integration for pytest
- pytest-cov - Coverage reporting
- black - Code formatting
- isort - Import sorting

### Running Tests

Run all tests:

```bash
pytest
```

Run with coverage report:

```bash
pytest --cov=coffee_admin --cov-report=html
```

Run specific test file:

```bash
pytest tests/test_views.py
```

Run specific test:

```bash
pytest tests/test_views.py::TestSearchAdminUrlsView::test_view_accessible_to_staff_user
```

Run with verbose output:

```bash
pytest -v
```

Run tests with markers:

```bash
pytest -m unit          # Run only unit tests
pytest -m permissions   # Run only permission tests
pytest -m views         # Run only view tests
```

### Test Structure

```
tests/
├── __init__.py
├── conftest.py          # Pytest fixtures and configuration
├── settings.py          # Test Django settings
├── urls.py              # Test URL configuration
├── test_app.py          # App configuration tests
└── test_views.py        # View and API tests
```

### Coverage

After running tests with coverage, open the HTML report:

```bash
# Generate coverage report
pytest --cov=coffee_admin --cov-report=html

# Open in browser (macOS)
open htmlcov/index.html

# Open in browser (Linux)
xdg-open htmlcov/index.html
```

### Writing Tests

The test suite includes:

- **Unit Tests** - App configuration, static files, templates
- **View Tests** - SearchAdminUrlsView, permission checks
- **Integration Tests** - Search API, JSON responses
- **Permission Tests** - Staff access, add permissions

Example test:

```python
import pytest

@pytest.mark.django_db
def test_search_view_accessible_to_staff(client, staff_user):
    """Staff users should be able to access search endpoint"""
    client.force_login(staff_user)
    response = client.get('/admin/coffee/search/')

    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'
```

### Continuous Integration

The test suite is designed to run in CI/CD pipelines:

```bash
# Install dependencies
pip install -e ".[test]"

# Run tests with coverage
pytest --cov=coffee_admin --cov-report=xml --cov-report=term

# Check coverage threshold (optional)
coverage report --fail-under=80
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Inspired by command launchers like:
- macOS Spotlight
- Alfred
- Raycast
- VS Code Command Palette

