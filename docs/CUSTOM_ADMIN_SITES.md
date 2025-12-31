# Using Coffee Admin with Custom AdminSite Implementations

The Coffee Admin package supports Django's custom AdminSite implementations, allowing you to use the launcher with multiple admin sites in the same project.

## Default Configuration

By default, the search view uses Django's default admin site (`admin.site`):

```python
# coffee_admin/urls.py (default)
from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.SearchAdminUrlsView.as_view(), name='search'),
]
```

## Using a Custom Admin Site

### Step 1: Create Your Custom Admin Site

```python
# myapp/admin.py
from django.contrib.admin import AdminSite

class MyCustomAdminSite(AdminSite):
    site_header = 'My Custom Admin'
    site_title = 'My Admin Portal'
    index_title = 'Welcome to My Admin'

# Create an instance
my_admin_site = MyCustomAdminSite(name='myadmin')

# Register your models
from myapp.models import MyModel
my_admin_site.register(MyModel)
```

### Step 2: Configure URLs for Your Custom Admin Site

```python
# myproject/urls.py
from django.urls import path, include
from myapp.admin import my_admin_site
from coffee_admin.views import SearchAdminUrlsView

urlpatterns = [
    # Default Django admin
    path('admin/', admin.site.urls),

    # Custom admin site
    path('myadmin/', my_admin_site.urls),

    # Coffee admin search for custom site
    path('myadmin/coffee/search/',
         SearchAdminUrlsView.as_view(admin_site=my_admin_site),
         name='custom_admin_search'),
]
```

## Multiple Admin Sites

You can support multiple admin sites in the same project:

```python
# myapp/admin.py
from django.contrib.admin import AdminSite

# Admin site for staff
class StaffAdminSite(AdminSite):
    site_header = 'Staff Administration'
    name = 'staffadmin'

staff_admin_site = StaffAdminSite()

# Admin site for partners
class PartnerAdminSite(AdminSite):
    site_header = 'Partner Portal'
    name = 'partneradmin'

partner_admin_site = PartnerAdminSite()
```

```python
# myproject/urls.py
from django.urls import path
from myapp.admin import staff_admin_site, partner_admin_site
from coffee_admin.views import SearchAdminUrlsView

urlpatterns = [
    # Staff admin
    path('staff/', staff_admin_site.urls),
    path('staff/coffee/search/',
         SearchAdminUrlsView.as_view(admin_site=staff_admin_site)),

    # Partner admin
    path('partner/', partner_admin_site.urls),
    path('partner/coffee/search/',
         SearchAdminUrlsView.as_view(admin_site=partner_admin_site)),
]
```

## Advanced: Dynamic Admin Site Selection

For more complex scenarios, you can override the `get_admin_site()` method:

```python
# myapp/views.py
from coffee_admin.views import SearchAdminUrlsView
from myapp.admin import staff_admin_site, partner_admin_site

class DynamicAdminSearchView(SearchAdminUrlsView):
    """
    Dynamically select admin site based on user permissions.
    """
    def get_admin_site(self):
        if self.request.user.groups.filter(name='Partners').exists():
            return partner_admin_site
        return staff_admin_site
```

## JavaScript Configuration

Update the JavaScript search URL to point to your custom admin site's search endpoint:

```javascript
// In your custom template or JavaScript
// Change the search URL in performSearch function
var searchUrl = '/myadmin/coffee/search/?q=' + encodeURIComponent(query);
```

Or override the entire `performSearch` function in your template:

```html
{% block extrahead %}
{{ block.super }}
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Override the search URL for custom admin site
    if (window.CoffeeAdmin) {
        var originalPerformSearch = window.CoffeeAdmin.performSearch;
        // Update search endpoint to custom admin site
    }
});
</script>
{% endblock %}
```

## Benefits

- ✅ **Multiple Admin Sites**: Use different launchers for different admin sites
- ✅ **Isolated Registries**: Each admin site has its own model registry
- ✅ **Custom Branding**: Each site can have different styling and branding
- ✅ **Permission Separation**: Different user groups can access different admin sites
- ✅ **URL Namespacing**: Clean URL structure for each admin site

## Complete Example

```python
# myapp/admin.py
from django.contrib.admin import AdminSite
from myapp.models import Product, Order

class EcommerceAdminSite(AdminSite):
    site_header = 'E-Commerce Admin'
    site_title = 'Shop Admin'
    index_title = 'Manage Your Store'
    name = 'shop'

ecommerce_admin = EcommerceAdminSite()
ecommerce_admin.register(Product)
ecommerce_admin.register(Order)
```

```python
# myproject/urls.py
from django.urls import path
from myapp.admin import ecommerce_admin
from coffee_admin.views import SearchAdminUrlsView

urlpatterns = [
    # E-commerce admin with coffee launcher
    path('shop/admin/', ecommerce_admin.urls),
    path('shop/admin/coffee/search/',
         SearchAdminUrlsView.as_view(admin_site=ecommerce_admin),
         name='shop_search'),
]
```

Now when you press Ctrl+D in the shop admin, it will only search through Products and Orders!
