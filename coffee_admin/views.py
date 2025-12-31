from django.shortcuts import render
from django.http import JsonResponse
from django.urls import get_resolver
from django.contrib import admin
from django.apps import apps
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin


class StaffMemberRequiredMixin(UserPassesTestMixin):
    """
    Mixin that requires the user to be a staff member.
    """
    def test_func(self):
        return self.request.user.is_active and self.request.user.is_staff


class AdminDashboardView(StaffMemberRequiredMixin, TemplateView):
    """
    Example admin-only view.
    This view is only accessible to staff members.
    """
    template_name = 'coffee_admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Coffee Admin Dashboard'
        return context


class SearchAdminUrlsView(StaffMemberRequiredMixin, View):
    """
    Search Django admin URLs and return matching results as JSON.
    Returns all registered admin pages with their titles and URLs.

    Supports custom AdminSite implementations by setting the admin_site attribute.

    Example with custom admin site:
        from myapp.admin import my_admin_site

        urlpatterns = [
            path('search/', SearchAdminUrlsView.as_view(admin_site=my_admin_site)),
        ]
    """
    # Default to Django's default admin site, can be overridden
    admin_site = admin.site

    def get_admin_site(self):
        """
        Get the admin site to search. Can be overridden for custom logic.
        """
        return self.admin_site

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').lower().strip()
        results = []

        # Get the admin site (supports custom implementations)
        admin_site = self.get_admin_site()

        # Get all registered models in admin
        for model, model_admin in admin_site._registry.items():
            try:
                app_label = model._meta.app_label
                model_name = model._meta.model_name

                # Safely get verbose names with fallbacks
                verbose_name = getattr(model._meta, 'verbose_name', model_name.replace('_', ' '))
                verbose_name_plural = getattr(model._meta, 'verbose_name_plural', verbose_name + 's')

                # Get the admin site's URL prefix
                admin_url = getattr(admin_site, 'name', 'admin')

                # Base URLs for this model
                list_url = f'/{admin_url}/{app_label}/{model_name}/'
                add_url = f'/{admin_url}/{app_label}/{model_name}/add/'

                # Create result for the model list view
                list_item = {
                    'title': verbose_name_plural.title(),
                    'subtitle': f'View all {verbose_name_plural}',
                    'url': list_url,
                    'icon': get_model_icon(app_label, model_name),
                    'category': 'models',
                    'app_label': app_label,
                }

                # Check if user has add permission for this model
                has_add_permission = model_admin.has_add_permission(request)

                # Create result for add view only if user has permission
                add_item = None
                if has_add_permission:
                    add_item = {
                        'title': f'Add {verbose_name.title()}',
                        'subtitle': f'Create a new {verbose_name}',
                        'url': add_url,
                        'icon': '➕',
                        'category': 'actions',
                        'app_label': app_label,
                    }

                # Filter results based on query
                if not query:
                    results.append(list_item)
                    if add_item:
                        results.append(add_item)
                else:
                    # Search in title, subtitle, and app label
                    list_searchable = f"{list_item['title']} {list_item['subtitle']} {app_label}".lower()

                    if query in list_searchable:
                        results.append(list_item)

                    if add_item:
                        add_searchable = f"{add_item['title']} {add_item['subtitle']} {app_label}".lower()
                        if query in add_searchable:
                            results.append(add_item)
            except Exception as e:
                # Skip models that cause errors
                continue

        # Add admin home (use the admin site's name for the URL)
        admin_url = getattr(admin_site, 'name', 'admin')
        if not query or 'home' in query or 'admin' in query or 'index' in query:
            results.insert(0, {
                'title': 'Admin Home',
                'subtitle': 'Django administration index',
                'url': f'/{admin_url}/',
                'icon': '🏠',
                'category': 'navigation',
                'app_label': 'admin',
            })

        # Limit results to prevent overwhelming the UI
        max_results = 50
        if len(results) > max_results:
            results = results[:max_results]

        return JsonResponse({
            'results': results,
            'query': query,
            'count': len(results),
        })


def get_model_icon(app_label, model_name):
    """
    Return an icon emoji for a model based on common patterns.
    """
    icon_map = {
        'auth': {
            'user': '👤',
            'group': '👥',
            'permission': '🔐',
        },
        'contenttypes': {
            'contenttype': '📋',
        },
        'sessions': {
            'session': '🔑',
        },
        'sites': {
            'site': '🌐',
        },
        'admin': {
            'logentry': '📝',
        },
    }

    # Try to find specific icon for this model
    if app_label in icon_map and model_name in icon_map[app_label]:
        return icon_map[app_label][model_name]

    # Generic icons based on app
    app_icons = {
        'auth': '🔐',
        'contenttypes': '📋',
        'sessions': '🔑',
        'sites': '🌐',
        'admin': '⚙️',
    }

    if app_label in app_icons:
        return app_icons[app_label]

    # Default icon
    return '📦'

