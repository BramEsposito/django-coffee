"""
Tests for coffee_admin app configuration
"""
import pytest
from django.apps import apps
from django.conf import settings


@pytest.mark.unit
class TestAppConfig:
    """Tests for CoffeeAdminConfig"""

    def test_app_installed(self):
        """Test that coffee_admin is in INSTALLED_APPS"""
        assert 'coffee_admin' in settings.INSTALLED_APPS

    def test_app_config(self):
        """Test that app config is correctly registered"""
        app_config = apps.get_app_config('coffee_admin')

        assert app_config.name == 'coffee_admin'
        assert app_config.verbose_name == 'Coffee Admin'

    def test_app_before_admin(self):
        """Test that coffee_admin is before django.contrib.admin"""
        installed_apps = list(settings.INSTALLED_APPS)
        coffee_index = installed_apps.index('coffee_admin')
        admin_index = installed_apps.index('django.contrib.admin')

        # coffee_admin should come before django.contrib.admin for template overrides
        assert coffee_index < admin_index


@pytest.mark.unit
class TestStaticFiles:
    """Tests for static files"""

    def test_static_files_exist(self):
        """Test that required static files exist"""
        import os
        from django.apps import apps

        app_config = apps.get_app_config('coffee_admin')
        static_dir = os.path.join(app_config.path, 'static', 'coffee_admin')

        # Check for CSS file
        css_file = os.path.join(static_dir, 'css', 'launcher.css')
        assert os.path.exists(css_file), f"CSS file not found at {css_file}"

        # Check for JS file
        js_file = os.path.join(static_dir, 'js', 'coffee_admin.js')
        assert os.path.exists(js_file), f"JS file not found at {js_file}"


@pytest.mark.unit
class TestTemplates:
    """Tests for templates"""

    def test_template_files_exist(self):
        """Test that required template files exist"""
        import os
        from django.apps import apps

        app_config = apps.get_app_config('coffee_admin')
        templates_dir = os.path.join(app_config.path, 'templates', 'admin')

        # Check for base_site.html override
        template_file = os.path.join(templates_dir, 'base_site.html')
        assert os.path.exists(template_file), f"Template file not found at {template_file}"

    def test_base_site_template_loads_static_files(self):
        """Test that base_site.html loads required static files"""
        import os
        from django.apps import apps

        app_config = apps.get_app_config('coffee_admin')
        template_file = os.path.join(app_config.path, 'templates', 'admin', 'base_site.html')

        with open(template_file, 'r') as f:
            content = f.read()

        # Should load static tag
        assert '{% load static %}' in content

        # Should include CSS
        assert 'launcher.css' in content

        # Should include JS
        assert 'coffee_admin.js' in content
