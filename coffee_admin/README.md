# Coffee Admin

A Django package designed to be loaded only in the Admin interface, without any database models.

## Features

- Admin-only interface
- No database models required
- Spotlight/Alfred-style command launcher with keyboard shortcuts
- JSON API for searching admin URLs
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

**IMPORTANT:** The `coffee_admin` URL pattern must be registered **before** the main `admin/` URL pattern to ensure proper routing.

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Coffee admin URLs must come BEFORE admin URLs
    path('admin/coffee/', include('coffee_admin.urls')),
    path('admin/', admin.site.urls),
]
```

### Custom Admin Views

The package includes example custom admin views that don't require models:

- `custom_admin_view`: A basic admin view example
- `admin_dashboard`: A staff-only dashboard view

### Launcher UI

The package includes a Spotlight/Alfred-style command launcher that can be triggered with a keyboard shortcut (default: Ctrl+D):

- **Search Admin Pages**: Type to search through all registered Django admin models and actions
- **Keyboard Shortcuts**:
  - `Ctrl+D` - Toggle launcher
  - `ESC` - Close launcher
  - `↑`/`↓` - Navigate through results
  - `Enter` - Select highlighted result and navigate

The launcher automatically searches all registered admin models and provides quick access to:
- Model list views (e.g., "Users", "Groups")
- Add new item views (e.g., "Add User")
- Admin home page

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

### JavaScript Integration

The package automatically loads a JavaScript file (`coffee_admin.js`) on every admin page. This file includes:

- Spotlight/Alfred-style launcher UI
- Configurable keyboard shortcuts
- Console logging to verify it's loaded
- A global `CoffeeAdmin` object for extending functionality

**Public API:**
```javascript
window.CoffeeAdmin.showLauncher()    // Show the launcher
window.CoffeeAdmin.hideLauncher()    // Hide the launcher
window.CoffeeAdmin.toggleLauncher()  // Toggle launcher visibility
```

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
├── urls.py            # URL routing (includes /search/ endpoint)
├── views.py           # Custom admin views and search API
├── static/
│   └── coffee_admin/
│       ├── css/
│       │   └── launcher.css     # Launcher UI styles
│       └── js/
│           └── coffee_admin.js  # Launcher and keyboard shortcuts
├── templates/
│   ├── admin/
│   │   └── base_site.html       # Template override for JS/CSS loading
│   └── coffee_admin/
│       └── dashboard.html
└── README.md
```

## Requirements

- Django 3.2+
- Python 3.8+

## License

See main project LICENSE file.
