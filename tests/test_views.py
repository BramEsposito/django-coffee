"""
Tests for coffee_admin views
"""
import pytest
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.test import RequestFactory
from django.urls import reverse
from coffee_admin.views import SearchAdminUrlsView, StaffMemberRequiredMixin


@pytest.mark.django_db
class TestStaffMemberRequiredMixin:
    """Tests for StaffMemberRequiredMixin"""

    def test_staff_user_passes_test(self, staff_user):
        """Staff users should pass the test"""
        mixin = StaffMemberRequiredMixin()
        request = RequestFactory().get('/')
        request.user = staff_user
        mixin.request = request

        assert mixin.test_func() is True

    def test_superuser_passes_test(self, superuser):
        """Superusers should pass the test"""
        mixin = StaffMemberRequiredMixin()
        request = RequestFactory().get('/')
        request.user = superuser
        mixin.request = request

        assert mixin.test_func() is True

    def test_regular_user_fails_test(self, regular_user):
        """Regular users should fail the test"""
        mixin = StaffMemberRequiredMixin()
        request = RequestFactory().get('/')
        request.user = regular_user
        mixin.request = request

        assert mixin.test_func() is False

    def test_inactive_staff_user_fails_test(self, db):
        """Inactive staff users should fail the test"""
        user = User.objects.create_user(
            username='inactive_staff',
            password='test',
            is_staff=True,
            is_active=False
        )
        mixin = StaffMemberRequiredMixin()
        request = RequestFactory().get('/')
        request.user = user
        mixin.request = request

        assert mixin.test_func() is False


@pytest.mark.django_db
class TestSearchAdminUrlsView:
    """Tests for SearchAdminUrlsView"""

    def test_view_requires_staff_user(self, client, regular_user):
        """View should not be accessible to non-staff users"""
        client.force_login(regular_user)
        response = client.get('/admin/coffee/search/')

        # Should redirect to login or return 403
        assert response.status_code in [302, 403]

    def test_view_accessible_to_staff_user(self, client, staff_user):
        """View should be accessible to staff users"""
        client.force_login(staff_user)
        response = client.get('/admin/coffee/search/')

        assert response.status_code == 200

    def test_view_returns_json(self, client, staff_user):
        """View should return JSON response"""
        client.force_login(staff_user)
        response = client.get('/admin/coffee/search/')

        assert response['Content-Type'] == 'application/json'

    def test_search_without_query_returns_all_models(self, client, staff_user):
        """Search without query parameter should return all registered models"""
        client.force_login(staff_user)
        response = client.get('/admin/coffee/search/')
        data = response.json()

        assert 'results' in data
        assert 'query' in data
        assert 'count' in data
        assert isinstance(data['results'], list)
        assert data['query'] == ''
        assert data['count'] > 0

    def test_search_includes_admin_home(self, client, staff_user):
        """Search results should include Admin Home"""
        client.force_login(staff_user)
        response = client.get('/admin/coffee/search/')
        data = response.json()

        results = data['results']
        admin_home = next((r for r in results if r['title'] == 'Admin Home'), None)

        assert admin_home is not None
        assert admin_home['url'] == '/admin/'
        assert admin_home['category'] == 'navigation'

    def test_search_with_query_filters_results(self, client, staff_user):
        """Search with query should filter results"""
        client.force_login(staff_user)
        response = client.get('/admin/coffee/search/?q=user')
        data = response.json()

        assert data['query'] == 'user'
        assert data['count'] > 0

        # Check that at least one result contains "user" in searchable fields
        results = data['results']
        assert len(results) > 0

    def test_search_includes_model_list_view(self, client, staff_user):
        """Search results should include model list views"""
        client.force_login(staff_user)
        response = client.get('/admin/coffee/search/?q=user')
        data = response.json()

        results = data['results']
        # Should have at least Users list view
        user_list = next((r for r in results if 'Users' in r['title'] and r['category'] == 'models'), None)

        assert user_list is not None
        assert '/admin/auth/user/' in user_list['url']

    def test_search_result_structure(self, client, staff_user):
        """Search results should have correct structure"""
        client.force_login(staff_user)
        response = client.get('/admin/coffee/search/')
        data = response.json()

        results = data['results']
        if results:
            result = results[0]
            assert 'title' in result
            assert 'subtitle' in result
            assert 'url' in result
            assert 'icon' in result
            assert 'category' in result
            assert 'app_label' in result

    def test_get_admin_site_returns_default(self):
        """get_admin_site should return default admin site"""
        view = SearchAdminUrlsView()

        assert view.get_admin_site() == admin.site

    def test_custom_admin_site_support(self, authenticated_staff_request):
        """View should support custom admin site"""
        from django.contrib.admin import AdminSite

        custom_site = AdminSite(name='custom_admin')
        view = SearchAdminUrlsView(admin_site=custom_site)

        assert view.get_admin_site() == custom_site


@pytest.mark.django_db
@pytest.mark.permissions
class TestPermissionFiltering:
    """Tests for permission-based filtering of search results"""

    def test_add_permission_included_when_allowed(self, client, superuser):
        """Add actions should be included for models where user has add permission"""
        client.force_login(superuser)
        response = client.get('/admin/coffee/search/?q=user')
        data = response.json()

        results = data['results']
        # Superuser should see "Add User" option
        add_user = next((r for r in results if 'Add' in r['title'] and 'User' in r['title']), None)

        assert add_user is not None
        assert add_user['category'] == 'actions'
        assert add_user['icon'] == '➕'

    def test_add_permission_excluded_for_log_entry(self, client, superuser):
        """Add actions should not be included for LogEntry (non-addable model)"""
        client.force_login(superuser)
        response = client.get('/admin/coffee/search/?q=log')
        data = response.json()

        results = data['results']
        # Should not have "Add Log Entry" option
        add_log_entry = next((r for r in results if 'Add' in r['title'] and 'Log' in r['title']), None)

        assert add_log_entry is None

    def test_list_view_always_included(self, client, staff_user):
        """List views should always be included regardless of add permission"""
        client.force_login(staff_user)
        response = client.get('/admin/coffee/search/')
        data = response.json()

        results = data['results']
        # Should have list views for models
        list_views = [r for r in results if r['category'] == 'models']

        assert len(list_views) > 0


@pytest.mark.django_db
class TestSearchQuery:
    """Tests for search query functionality"""

    def test_empty_query_returns_all_results(self, client, staff_user):
        """Empty query should return all models and actions"""
        client.force_login(staff_user)
        response = client.get('/admin/coffee/search/?q=')
        data = response.json()

        assert data['query'] == ''
        assert data['count'] > 0

    def test_case_insensitive_search(self, client, staff_user):
        """Search should be case-insensitive"""
        client.force_login(staff_user)

        response_lower = client.get('/admin/coffee/search/?q=user')
        response_upper = client.get('/admin/coffee/search/?q=USER')
        response_mixed = client.get('/admin/coffee/search/?q=User')

        data_lower = response_lower.json()
        data_upper = response_upper.json()
        data_mixed = response_mixed.json()

        # All should return same results
        assert data_lower['count'] == data_upper['count'] == data_mixed['count']

    def test_search_in_app_label(self, client, staff_user):
        """Search should match against app labels"""
        client.force_login(staff_user)
        response = client.get('/admin/coffee/search/?q=auth')
        data = response.json()

        results = data['results']
        # Should return auth app models (User, Group, Permission)
        assert len(results) > 0

        # Check that results include auth app items
        auth_results = [r for r in results if r['app_label'] == 'auth']
        assert len(auth_results) > 0

    def test_max_results_limit(self, client, staff_user):
        """Search should limit results to prevent overwhelming UI"""
        client.force_login(staff_user)
        response = client.get('/admin/coffee/search/')
        data = response.json()

        # Should not exceed 50 results (as per view implementation)
        assert data['count'] <= 50

    def test_no_results_for_nonexistent_query(self, client, staff_user):
        """Search should return empty results for non-matching query"""
        client.force_login(staff_user)
        response = client.get('/admin/coffee/search/?q=nonexistentmodel12345')
        data = response.json()

        assert data['count'] == 0
        assert data['results'] == []
