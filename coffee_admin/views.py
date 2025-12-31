from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.urls import get_resolver
from django.contrib import admin
from django.apps import apps


@staff_member_required
def admin_dashboard(request):
    """
    Example admin-only view.
    This view is only accessible to staff members.
    """
    context = {
        'title': 'Coffee Admin Dashboard',
    }
    return render(request, 'coffee_admin/dashboard.html', context)


@staff_member_required
def search_admin_urls(request):
    """
    Search Django admin URLs and return matching results as JSON.
    Returns all registered admin pages with their titles and URLs.
    """
    query = request.GET.get('q', '').lower().strip()

    results = []

    # Get all registered models in admin
    for model, model_admin in admin.site._registry.items():
        try:
            app_label = model._meta.app_label
            model_name = model._meta.model_name

            # Safely get verbose names with fallbacks
            verbose_name = getattr(model._meta, 'verbose_name', model_name.replace('_', ' '))
            verbose_name_plural = getattr(model._meta, 'verbose_name_plural', verbose_name + 's')

            # Base URLs for this model
            list_url = f'/admin/{app_label}/{model_name}/'
            add_url = f'/admin/{app_label}/{model_name}/add/'

            # Create result for the model list view
            list_item = {
                'title': verbose_name_plural.title(),
                'subtitle': f'View all {verbose_name_plural}',
                'url': list_url,
                'icon': get_model_icon(app_label, model_name),
                'category': 'models',
                'app_label': app_label,
            }

            # Create result for add view
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
            else:
                # Search in title, subtitle, and app label
                list_searchable = f"{list_item['title']} {list_item['subtitle']} {app_label}".lower()
                add_searchable = f"{add_item['title']} {add_item['subtitle']} {app_label}".lower()

                if query in list_searchable:
                    results.append(list_item)
                if query in add_searchable:
                    results.append(add_item)
        except Exception as e:
            # Skip models that cause errors
            continue

    # Add admin home
    if not query or 'home' in query or 'admin' in query or 'index' in query:
        results.insert(0, {
            'title': 'Admin Home',
            'subtitle': 'Django administration index',
            'url': '/admin/',
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
